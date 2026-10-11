#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幻想之境 Online — 遊戲伺服器

純 Python 標準函式庫實作 (HTTP + WebSocket + 遊戲邏輯),不需要安裝任何套件。
用法:  python server.py [port]     預設 port = 8000

遊戲數值 (寵物、技能、職業、道具、遇敵區域) 都在 game_data.py。
"""
import asyncio
import base64
import hashlib
import heapq
import json
import math
import os
import random
import secrets
import socket
import struct
import sys
import time
import traceback
from urllib.parse import parse_qs, unquote

from game_data import (ART, ART_FRAMES, BOSS, CARE, CLASSES, EGG_SHOP, ELEMENTS, ENCOUNTER_MIN_STEPS,
                       ENCOUNTER_RATE, FOODS, HATCH_HINTS, HATCH_TIME, HATCH_WARMUP, INTERACT, ITEMS, PET_SKILLS,
                       ROAD_ENCOUNTER, SHOP_ITEMS, SPECIES, STATUS_NAMES, TASTE, TASTE_NAMES, WEATHER, WILD_POWER,
                       WILD_QUALITY_WEIGHTS, ZONES, assist_mult, derive, disobey_chance, elem_mult, exp_need,
                       link_ratio, pet_skills, stars, sync_gain, taste)

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

PORT = 8000
ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ROOT, 'public')
DATA_DIR = os.environ.get('FANTASIA_DATA') or os.path.join(ROOT, 'data')   # 測試時可以指定別的存檔資料夾
SAVE_FILE = os.path.join(DATA_DIR, 'players.json')

TICK = 0.05        # 伺服器邏輯 20 Hz
SNAP_EVERY = 2     # 每 2 tick 送一次畫面快照 (10 Hz)
VIEW = 22          # 玩家視野範圍 (格)
INV_MAX = 24
PET_MAX = 5        # 身上最多帶幾隻寵物 (封印卡欄位)
PARTY_MAX = 6      # 一場戰鬥最多幾位玩家
PET_TIMEOUT = 6.0  # 寵物時間棒集滿後幾秒沒下指令就自動普攻
WS_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

TELEPORTS = [('南方草原', 48.5, 66.5, 50), ('東方森林', 74.5, 48.5, 120), ('北方焦土', 72.5, 15.5, 300)]

NPCS = [
    {'i': 1, 'n': '村長 艾倫', 'x': 44.5, 'y': 44.5, 'c': 'elder'},
    {'i': 2, 'n': '道具商人 莉莉', 'x': 51.5, 'y': 44.5, 'c': 'merchant'},
    {'i': 3, 'n': '修女 瑪莉', 'x': 44.5, 'y': 52.5, 'c': 'healer'},
    {'i': 4, 'n': '傳送師 奧茲', 'x': 51.5, 'y': 52.5, 'c': 'wizard'},
    {'i': 5, 'n': '孵化屋 葛莉絲婆婆', 'x': 42.5, 'y': 48.5, 'c': 'hatcher'},
    {'i': 6, 'n': '寵物旅館 蘿絲', 'x': 53.5, 'y': 50.5, 'c': 'keeper'},
]
NPC_DLG = {
    'elder': ('歡迎來到艾爾文村,年輕的訓練師!\n'
              '村外的野地藏著許多野生寵物,走著走著就會遇上牠們。\n'
              '把牠們打到虛弱,再丟出「封印卡」,就能收服成自己的夥伴。\n'
              '越往外走寵物越強……北方焦土還沉睡著一頭炎龍。\n'
              '對了,寵物也會肚子餓、會鬧脾氣。好好照顧牠們,牠們也會拚命保護你。', [['close', '我知道了']]),
    'merchant': ('歡迎光臨~封印卡、藥水、復活草都有喔!\n寵物的食物也有賣,每種寵物愛吃的東西不一樣喔。\n'
                 '出門抓寵物,封印卡可要帶夠!', [['shop', '我要買東西'], ['close', '不用了']]),
    'healer': ('願女神祝福你與你的夥伴們。\n需要我為你們治療嗎?', [['heal', '請治療我和寵物 (免費)'], ['close', '不用了']]),
    'wizard': ('我可以用魔法把你傳送到遠方……\n當然,要收一點點費用。',
               [['tp:%d' % i, '%s (%d 金幣)' % (t[0], t[3])] for i, t in enumerate(TELEPORTS)] + [['close', '算了']]),
    'hatcher': ('呵呵呵,我是孵化屋的葛莉絲。\n每一顆蛋都有自己喜歡的溫度和濕度,\n照顧得越好,孵出來的孩子素質越好喔。\n'
                '我也會收購寵物,不想養的可以賣給我。',
                [['eggs', '購買寵物蛋'], ['hatch', '我要孵蛋'], ['sellpet', '賣寵物'], ['hint', '孵蛋有什麼訣竅?'],
                 ['close', '下次再說']]),
    'keeper': ('歡迎來到寵物旅館~我是老闆娘蘿絲。\n帶不下的寵物可以寄放在這裡,免費喔!\n'
               '住在旅館的孩子每天都在後院玩,心情會慢慢變好。',
               [['bank', '寄放 / 領回寵物'], ['bankinfo', '旅館是做什麼的?'], ['close', '下次再說']]),
}

# ============================================================
#  地圖
# ============================================================
W = H = 96
T_GRASS, T_WATER, T_TREE, T_SAND, T_STONE, T_WALL, T_FLOWER, T_DARK, T_BRIDGE, T_ASH = range(10)
BLOCKED = {T_WATER, T_TREE, T_WALL}
CENTER = (48, 48)
SPAWN = (48.0, 50.5)
LAIR = (80, 14)


def make_noise(seed):
    def h(ix, iy):
        n = (ix * 374761393 + iy * 668265263 + seed * 982451653) & 0xffffffff
        n = ((n ^ (n >> 13)) * 1274126177) & 0xffffffff
        return ((n ^ (n >> 16)) & 0xffff) / 65535.0

    def noise(x, y):
        ix, iy = math.floor(x), math.floor(y)
        fx, fy = x - ix, y - iy
        sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        a, b, c, d = h(ix, iy), h(ix + 1, iy), h(ix, iy + 1), h(ix + 1, iy + 1)
        top = a + (b - a) * sx
        bot = c + (d - c) * sx
        return top + (bot - top) * sy
    return noise


def gen_map(seed=2003):
    wn, fn = make_noise(seed + 1), make_noise(seed + 2)
    rnd = random.Random(seed)
    tiles = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - CENTER[0], y - CENTER[1])
            t = T_DARK if d > 36 else T_GRASS
            wv = wn(x / 10.0, y / 10.0) * 0.7 + wn(x / 4.0 + 50, y / 4.0) * 0.3
            fv = fn(x / 7.0, y / 7.0) * 0.7 + fn(x / 3.0 + 50, y / 3.0) * 0.3
            if wv > 0.70:
                t = T_WATER
            elif fv > 0.66:
                t = T_TREE
            elif rnd.random() < (0.025 if d <= 36 else 0.004):
                t = T_FLOWER
            tiles[y * W + x] = t

    # 炎龍巢穴 (焦土)
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - LAIR[0], y - LAIR[1])
            if d < 7.5:
                tiles[y * W + x] = T_ASH
            elif d < 9 and tiles[y * W + x] in BLOCKED:
                tiles[y * W + x] = T_DARK

    # 艾爾文村 (城牆 + 石板地 + 噴水池)
    for y in range(37, 59):
        for x in range(37, 59):
            tiles[y * W + x] = T_GRASS
    for y in range(40, 56):
        for x in range(40, 56):
            tiles[y * W + x] = T_STONE if (40 < x < 55 and 40 < y < 55) else T_WALL
    for k in (47, 48):
        tiles[40 * W + k] = tiles[55 * W + k] = T_STONE
        tiles[k * W + 40] = tiles[k * W + 55] = T_STONE
    for (x, y) in ((47, 44), (48, 44), (47, 45), (48, 45)):
        tiles[y * W + x] = T_WATER
    for (x, y) in ((41, 41), (54, 41), (41, 54), (54, 54)):
        tiles[y * W + x] = T_FLOWER

    # 道路 (遇水搭橋)
    def road(x, y):
        i = y * W + x
        tiles[i] = T_BRIDGE if tiles[i] == T_WATER else T_SAND
    for y in range(1, 40):
        road(47, y); road(48, y)
    for y in range(56, H - 1):
        road(47, y); road(48, y)
    for x in range(1, 40):
        road(x, 47); road(x, 48)
    for x in range(56, W - 1):
        road(x, 47); road(x, 48)
    for x in range(49, 74):
        road(x, 14); road(x, 15)

    # 地圖邊界
    for i in range(W):
        tiles[i] = tiles[(H - 1) * W + i] = T_TREE
        tiles[i * W] = tiles[i * W + W - 1] = T_TREE
    return tiles


def in_town(x, y, m=0.0):
    return 40 - m <= x < 56 + m and 40 - m <= y < 56 + m


def dist(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)


def hash_pw(salt, pw):
    return hashlib.sha256((salt + pw).encode('utf-8')).hexdigest()


def wpick(weights):
    r = random.random() * sum(weights)
    for i, w in enumerate(weights):
        r -= w
        if r <= 0:
            return i
    return len(weights) - 1


NEIGH = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
         (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]


# ============================================================
#  寵物
# ============================================================
def clamp(v, lo=0.0, hi=100.0):
    return lo if v < lo else hi if v > hi else v


def new_pet(sp, lv, q, name=None, start='new'):
    """建立一隻寵物。q = 天生素質點 (0~12),依種族偏好隨機分配到四項能力
    start = new 新手送的 / hatch 孵化 / wild 捕捉,決定飽食度、快樂值、親密度的起始值"""
    s = SPECIES[sp]
    st = list(s['base'])
    w = [p + 1 for p in s['pref']]
    for _ in range(q):
        st[wpick(w)] += 1
    d = derive(lv, st)
    food, joy, bond = CARE['start_' + start]
    if isinstance(bond, tuple):
        bond = random.randint(*bond)
    return {'uid': secrets.token_hex(4), 'sp': sp, 'n': name or s['name'], 'lv': lv, 'exp': 0, 'q': q,
            'st': st, 'pts': s['grow'] * (lv - 1), 'hp': d['mhp'], 'mp': d['mmp'],
            'food': float(food), 'joy': float(joy), 'bond': float(bond), 'sync': 0.0}


def pet_ok(pt):
    try:
        return (pt['sp'] in SPECIES and len(pt['st']) == 4 and int(pt['lv']) >= 1)
    except Exception:
        return False


def fix_pet(pt):
    """舊存檔 (階段 1) 的寵物沒有照顧數值,補上預設值"""
    food, joy, bond = CARE['start_old']
    for k, v in (('food', food), ('joy', joy), ('bond', bond), ('sync', 0)):
        try:
            pt[k] = float(clamp(float(pt.get(k, v))))
        except (TypeError, ValueError):
            pt[k] = float(v)
    pt['sulk'] = bool(pt.get('sulk', False))
    return pt


def pet_view(pt):
    d = derive(pt['lv'], pt['st'])
    return {'uid': pt['uid'], 'sp': pt['sp'], 'n': pt['n'], 'lv': pt['lv'], 'exp': pt['exp'], 'nx': exp_need(pt['lv']),
            'q': pt['q'], 'star': stars(pt['q']), 'st': pt['st'], 'pts': pt['pts'], 'hp': pt['hp'], 'mp': pt['mp'],
            'mhp': d['mhp'], 'mmp': d['mmp'], 'atk': d['atk'], 'matk': d['matk'], 'def': d['def'], 'mdef': d['mdef'],
            'spd': round(d['spd'], 1), 'skills': pet_skills(pt['sp'], pt['lv']),
            'food': int(math.ceil(pt['food'])), 'joy': int(math.ceil(pt['joy'])), 'bond': int(pt['bond']),
            'sync': int(pt['sync']), 'sulk': int(pt.get('sulk', False))}


def pet_price(pt):
    return 30 + pt['lv'] * 15 + pt['q'] * 25 + (100 if 'egg' in SPECIES[pt['sp']] else 0)


def can_fight(pt):
    return pt['hp'] > 0 and pt['food'] > 0


def pet_mood(pt, idle=0.0):
    """心情泡泡 (地圖上):依優先順序取第一個符合的"""
    if pt['food'] <= 0:
        return 'starve'
    if pt['food'] < CARE['hungry']:
        return 'hungry'
    if pt['joy'] < CARE['angry']:
        return 'angry'
    if idle >= CARE['sleepy_idle']:
        return 'sleepy'
    if pt['joy'] >= CARE['love_joy'] and pt['bond'] >= CARE['love_bond']:
        return 'love'
    return ''


def live_cd(cd, now):
    """互動冷卻:只留還沒結束的 (存檔與讀檔用)"""
    out = {}
    for uid, cds in (cd or {}).items() if isinstance(cd, dict) else ():
        if isinstance(cds, dict):
            left = {a: float(t) for a, t in cds.items() if isinstance(t, (int, float)) and t > now}
            if left:
                out[str(uid)] = left
    return out


# ============================================================
#  玩家
# ============================================================
class Player:
    def __init__(self, pid, name, rec, ws):
        self.id = pid
        self.name = name
        self.ws = ws
        self.rec = rec
        self.cls = rec['cls']
        self.lv = int(rec.get('lv', 1))
        self.exp = int(rec.get('exp', 0))
        self.gold = int(rec.get('gold', 0))
        self.inv = [{'id': s['id'], 'n': int(s['n'])} for s in rec.get('inv', [])
                    if isinstance(s, dict) and s.get('id') in ITEMS][:INV_MAX]
        self.pets = [fix_pet(pt) for pt in rec.get('pets', []) if pet_ok(pt)][:PET_MAX]
        self.bank = [fix_pet(pt) for pt in rec.get('bank', []) if pet_ok(pt)]   # 寄放在寵物旅館的寵物
        self.active = min(max(0, int(rec.get('active', 0))), max(0, len(self.pets) - 1))
        self.x, self.y = float(rec.get('x', SPAWN[0])), float(rec.get('y', SPAWN[1]))
        self.recalc()
        self.hp = max(1, min(self.mhp, int(rec.get('hp', self.mhp))))
        self.mp = min(self.mmp, int(rec.get('mp', self.mmp)))
        self.face, self.moving, self.dir = 1, False, (0.0, 0.0)
        self.path, self.repath_at = [], 0.0
        self.npc = None
        self.boss_go = False
        self.battle = None
        self.btarget = 0          # 戰鬥中選定的敵人
        self.auto = False         # 自動戰鬥
        self.enc_dist, self.steps = 0.0, ENCOUNTER_MIN_STEPS
        self.hatch = None
        self.last_chat = 0.0
        self.cd = live_cd(rec.get('cd'), time.time())   # 寵物 uid → {互動動作: 冷卻結束時間} (會存檔,重新登入不會重置)
        self.sulk = {}            # 寵物 uid → 快樂值與飽食度都是 0 持續了幾秒
        self.idle_since = time.time()
        self.care_n = 0
        self.inv_dirty = self.pets_dirty = self.bank_dirty = True

    def remove_pet(self, i):
        """從身上移除第 i 隻寵物,並修正出戰寵物的索引"""
        pt = self.pets.pop(i)
        if i < self.active:
            self.active -= 1
        self.active = min(max(0, self.active), max(0, len(self.pets) - 1))
        self.pets_dirty = True
        return pt

    def recalc(self):
        c, l = CLASSES[self.cls], self.lv - 1
        self.mhp = int(c['hp'] + c['ghp'] * l)
        self.mmp = int(c['mp'] + c['gmp'] * l)
        self.spd = 4.2

    def clear_actions(self):
        self.npc = None
        self.boss_go = False
        self.path = []

    def alive_pet(self):
        """回傳可以出戰的寵物索引 (優先用目前的出戰寵物)。倒下或餓昏的寵物不能出戰"""
        if 0 <= self.active < len(self.pets) and can_fight(self.pets[self.active]):
            return self.active
        for i, pt in enumerate(self.pets):
            if can_fight(pt):
                return i
        return None

    def record(self):
        r = dict(self.rec)
        r.update({'cls': self.cls, 'lv': self.lv, 'exp': self.exp, 'gold': self.gold, 'inv': self.inv,
                  'pets': self.pets, 'bank': self.bank, 'active': self.active, 'x': round(self.x, 2), 'y': round(self.y, 2),
                  'hp': self.hp, 'mp': self.mp, 'last': int(time.time()), 'cd': live_cd(self.cd, time.time())})
        r.pop('equip', None)
        return r


# ============================================================
#  戰鬥單位與戰鬥
# ============================================================
class Unit:
    def __init__(self, uid, side, kind, name, lv):
        self.id, self.side, self.kind, self.name, self.lv = uid, side, kind, name, lv  # kind: o 主人 / p 寵物 / m 敵人
        self.el = self.sp = self.cls = self.pid = self.pet = None
        self.mhp = self.mmp = self.hp = self.mp = 1
        self.atk = self.matk = self.df = self.mdf = 0
        self.spd, self.eva = 20.0, 0.0
        self.bar, self.ready_at = 0.0, None
        self.status, self.shield, self.next_poison = {}, 0, 0.0
        self.stmul = {}           # 狀態的強度 (助攻加成用,預設 1)
        self.skills, self.alive, self.row, self.q = [], True, 0, 0
        self.boss, self.acts, self.exp, self.gold = False, 0, 0, 0
        self.sync, self.surge = 0.0, False   # 默契量表、助攻發動後的下一招

    def set_stats(self, d):
        self.mhp, self.mmp = d['mhp'], d['mmp']
        self.atk, self.matk, self.df, self.mdf = d['atk'], d['matk'], d['def'], d['mdef']
        self.spd, self.eva = d['spd'], d['eva']

    def rate(self):
        if not self.alive or self.ready_at is not None or 'sleep' in self.status:
            return 0.0
        return self.spd * smod(self, 'haste', 1.35) * smod(self, 'slow', 0.6)


class Battle:
    def __init__(self, bid, cx, cy, boss=False):
        self.id, self.cx, self.cy, self.boss = bid, cx, cy, boss
        self.units = {}
        self.pids = []         # 參戰玩家 (加入順序 = 站位排數)
        self.ou, self.pu = {}, {}   # pid → 主人單位 id / 寵物單位 id
        self.fought = {}       # pid → 參戰過的寵物 uid
        self.weather, self.weather_until = None, 0.0
        self.over = False
        self.exp = self.gold = 0
        self.loot = []

    def add(self, u):
        self.units[u.id] = u
        return u

    def alive(self, side):
        return [u for u in self.units.values() if u.side == side and u.alive]


def smod(u, key, k):
    """狀態倍率。助攻加成會放大增加的幅度:例如攻↑ 1.3,加成 ×1.5 → 1.45"""
    if key not in u.status:
        return 1.0
    return 1 + (k - 1) * u.stmul.get(key, 1.0)


# ============================================================
#  遊戲世界
# ============================================================
class Game:
    def __init__(self):
        self.tiles = gen_map()
        self.block = bytearray(1 if t in BLOCKED else 0 for t in self.tiles)
        self.tiles_str = ''.join(str(t) for t in self.tiles)
        self._id = 100
        self.players, self.by_name = {}, {}
        self.battles = {}
        self.fx = []
        self.npc_by_id = {n['i']: n for n in NPCS}
        self.boss = {'i': 99, 'x': LAIR[0] + 0.5, 'y': LAIR[1] + 0.5, 'alive': True, 'respawn_at': 0.0, 'battle': None}
        self.accounts = self.load()
        self.tickn = 0
        self.last_save = self.last_regen = time.time()

    def nid(self):
        self._id += 1
        return self._id

    # ---------- 存檔 ----------
    def load(self):
        try:
            with open(SAVE_FILE, encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception:
            traceback.print_exc()
            return {}

    def save(self):
        for p in self.players.values():
            self.accounts[p.name] = p.record()
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            tmp = SAVE_FILE + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(self.accounts, f, ensure_ascii=False, indent=1)
            os.replace(tmp, SAVE_FILE)
        except Exception:
            traceback.print_exc()

    # ---------- 地形 / 移動 ----------
    def walkable(self, x, y):
        if x < 0 or y < 0 or x >= W or y >= H:
            return False
        return not self.block[int(y) * W + int(x)]

    def can_stand(self, x, y, r=0.25):
        return (self.walkable(x - r, y - r) and self.walkable(x + r, y - r)
                and self.walkable(x - r, y + r) and self.walkable(x + r, y + r))

    def tile_at(self, x, y):
        return self.tiles[int(y) * W + int(x)]

    def find_path(self, sx, sy, gx, gy, limit=3000):
        if not (0 <= gx < W and 0 <= gy < H) or self.block[gy * W + gx]:
            return None
        start, goal = sy * W + sx, gy * W + gx
        if start == goal:
            return []
        openh = [(0.0, start)]
        came, g = {start: -1}, {start: 0.0}
        n = 0
        blk = self.block
        while openh:
            _, cur = heapq.heappop(openh)
            if cur == goal:
                break
            n += 1
            if n > limit:
                return None
            cx, cy = cur % W, cur // W
            for dx, dy, c in NEIGH:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    continue
                ni = ny * W + nx
                if blk[ni]:
                    continue
                if dx and dy and (blk[cy * W + nx] or blk[ny * W + cx]):
                    continue
                ng = g[cur] + c
                if ng < g.get(ni, 1e9):
                    g[ni] = ng
                    came[ni] = cur
                    ddx, ddy = abs(nx - gx), abs(ny - gy)
                    heapq.heappush(openh, (ng + max(ddx, ddy) + 0.414 * min(ddx, ddy), ni))
        if goal not in came:
            return None
        path, cur = [], goal
        while cur != start:
            path.append((cur % W + 0.5, cur // W + 0.5))
            cur = came[cur]
        path.reverse()
        return path

    def step(self, e, tx, ty, spd, dt):
        """朝 (tx, ty) 前進,會沿著障礙物滑動;回傳是否已抵達"""
        dx, dy = tx - e.x, ty - e.y
        d = math.hypot(dx, dy)
        if d < 1e-6:
            return True
        s = min(d, spd * dt)
        nx, ny = e.x + dx / d * s, e.y + dy / d * s
        if self.can_stand(nx, ny):
            e.x, e.y = nx, ny
        elif self.can_stand(nx, e.y):
            e.x = nx
        elif self.can_stand(e.x, ny):
            e.y = ny
        else:
            e.moving = False
            return False
        e.moving = True
        if abs(dx) > 0.05:
            e.face = 1 if dx > 0 else -1
        return d <= spd * dt

    def follow_path(self, e, spd, dt):
        if not e.path:
            return True
        wx, wy = e.path[0]
        before = (e.x, e.y)
        if self.step(e, wx, wy, spd, dt):
            e.path.pop(0)
        elif (e.x, e.y) == before:
            e.path = []
        return not e.path

    def chase(self, e, tx, ty, spd, dt, now):
        gx, gy = int(tx), int(ty)
        if (int(e.x) == gx and int(e.y) == gy) or dist(e.x, e.y, tx, ty) < 1.0:
            e.path = []
            return self.step(e, tx, ty, spd, dt)
        if now >= e.repath_at or not e.path:
            e.path = self.find_path(int(e.x), int(e.y), gx, gy) or []
            e.repath_at = now + 0.35
            if not e.path:
                return self.step(e, tx, ty, spd, dt)
        self.follow_path(e, spd, dt)
        return False

    # ---------- 訊息 ----------
    def add_fx(self, k, x, y, **kw):
        kw.update(k=k, x=round(x, 2), y=round(y, 2))
        self.fx.append(kw)

    def bfx(self, b, k, **kw):
        self.add_fx(k, b.cx, b.cy, b=b.id, **kw)

    def sys(self, p, text, ch='sys'):
        p.ws.send({'t': 'chat', 'ch': ch, 'm': text})

    def broadcast(self, msg):
        for p in self.players.values():
            p.ws.send(msg)

    def broadcast_sys(self, text, ch='sys'):
        self.broadcast({'t': 'chat', 'ch': ch, 'm': text})

    # ---------- 登入 / 登出 ----------
    def login(self, ws, m):
        name = str(m.get('name', '')).strip()[:12]
        pw = str(m.get('pass', ''))[:32]
        cls = m.get('cls')
        if len(name) < 2 or any(c in name for c in ' \t<>&"\'/\\'):
            ws.send({'t': 'err', 'm': '角色名稱需為 2~12 個字,且不能包含空白或特殊符號'})
            return None
        if name in self.by_name:
            ws.send({'t': 'err', 'm': '此角色已經在線上了'})
            return None
        rec = self.accounts.get(name)
        if rec and (rec.get('cls') not in CLASSES or 'pets' not in rec):
            rec = None   # 原型版本 (沒有寵物) 的角色資料,重新建立
        if rec:
            if hash_pw(rec['salt'], pw) != rec['hash']:
                ws.send({'t': 'err', 'm': '密碼錯誤!'})
                return None
            is_new = False
        else:
            if cls not in CLASSES:
                ws.send({'t': 'err', 'm': '請選擇職業'})
                return None
            salt = secrets.token_hex(8)
            rec = {'salt': salt, 'hash': hash_pw(salt, pw), 'cls': cls, 'lv': 1, 'exp': 0, 'gold': 300,
                   'inv': [{'id': 'seal_card', 'n': 5}, {'id': 'red_potion', 'n': 5}, {'id': 'blue_potion', 'n': 2}],
                   'pets': [new_pet('poring', 1, 4)], 'active': 0,
                   'x': SPAWN[0], 'y': SPAWN[1], 'created': int(time.time())}
            self.accounts[name] = rec
            is_new = True
        p = Player(self.nid(), name, rec, ws)
        if not self.can_stand(p.x, p.y):
            p.x, p.y = SPAWN
        self.players[p.id] = p
        self.by_name[name] = p
        if is_new:
            self.save()
        species = {k: {'n': v['name'], 'el': v['el'], 'fam': v['fam'], 'base': v['base'], 'grow': v['grow'],
                       'skills': v['skills'], 'egg': 'egg' in v, 'love': v.get('love'), 'hate': v.get('hate'),
                       'trick': v.get('trick')} for k, v in SPECIES.items()}
        classes = {k: {'n': v['name'], 'desc': v['desc'], 'skills': v['skills']} for k, v in CLASSES.items()}
        care = {k: CARE[k] for k in ('hungry', 'full', 'sync_bond', 'guard_bond', 'bank_max', 'assist')}
        care['trick_bond'] = INTERACT['trick']['need_bond']
        ws.send({'t': 'welcome', 'id': p.id, 'name': name, 'cls': p.cls, 'w': W, 'h': H, 'tiles': self.tiles_str,
                 'npcs': NPCS, 'species': species, 'classes': classes, 'pskills': PET_SKILLS, 'items': ITEMS,
                 'elements': ELEMENTS, 'statusNames': STATUS_NAMES, 'weather': {k: v['name'] for k, v in WEATHER.items()},
                 'hatchTime': HATCH_TIME, 'hatchWarmup': HATCH_WARMUP, 'petMax': PET_MAX,
                 'foods': list(FOODS), 'tasteNames': TASTE_NAMES, 'care': care, 'art': ART,
                 'interact': {k: {'n': v['name'], 'cd': v['cd']} for k, v in INTERACT.items()}})
        self.broadcast_sys('%s 進入了遊戲。' % name)
        if is_new:
            self.sys(p, '歡迎來到幻想之境!你的第一個夥伴是「噗噗」。按 P 可以查看寵物。')
            self.sys(p, '走出村莊就會遇到野生寵物。打到虛弱時用「封印卡」收服牠們吧!按 H 查看操作說明。')
            self.sys(p, '寵物也會肚子餓喔!噗噗最愛吃「莓果」,道具商人莉莉那裡買得到。')
        else:
            self.sys(p, '歡迎回來,%s!' % name)
            away = time.time() - float(rec.get('last', time.time()))
            if away >= CARE['miss_you'] and p.pets:
                pt = p.pets[p.active]
                self.sys(p, '%s 一看到你就撲了過來,看起來好想你!' % pt['n'])
                self.add_fx('pact', p.x, p.y, id=p.id, a='miss', r='ok', act=1, sp=pt['sp'])
        print('[登入] %s (%s) 線上人數 %d' % (name, CLASSES[p.cls]['name'], len(self.players)))
        return p

    def logout(self, p):
        b = self.battles.get(p.battle)
        if b:
            self.leave_battle(b, p, time.time())
        if p.hatch:   # 孵到一半離線:把蛋還回去
            self.add_item(p, p.hatch['egg'])
            p.hatch = None
        self.accounts[p.name] = p.record()
        self.players.pop(p.id, None)
        self.by_name.pop(p.name, None)
        self.save()
        self.broadcast_sys('%s 離開了遊戲。' % p.name)
        print('[登出] %s 線上人數 %d' % (p.name, len(self.players)))

    # ---------- 玩家指令 ----------
    def handle(self, p, m):
        t = m.get('t')
        now = time.time()
        if t == 'chat':
            return self.chat(p, m.get('m', ''), now)
        if t == 'ping':
            return p.ws.send({'t': 'pong', 'c': m.get('c')})
        if t == 'bcmd':
            return self.battle_cmd(p, m, now)
        if t == 'bauto':
            p.auto = bool(m.get('on'))
            return
        if t == 'btarget':
            p.btarget = int(m.get('id', 0))
            return
        if t == 'hknob':
            if p.hatch:
                p.hatch['kt'] = max(0.0, min(100.0, float(m.get('kt', 50))))
                p.hatch['kh'] = max(0.0, min(100.0, float(m.get('kh', 50))))
            return
        if t == 'pset':
            return self.pet_set_active(p, m.get('i'))
        if t == 'palloc':
            return self.pet_alloc(p, m.get('i'), m.get('s'), m.get('n', 1))
        if t == 'pauto':
            return self.pet_auto_alloc(p, m.get('i'))
        if t == 'pname':
            return self.pet_rename(p, m.get('i'), m.get('n', ''))
        if t == 'prelease':
            return self.pet_release(p, m.get('i'))
        if t == 'psell':
            return self.pet_sell(p, m.get('i'))
        if t == 'feed':
            return self.feed(p, m.get('i'), m.get('item'), now)
        if t == 'bput':
            return self.bank_put(p, m.get('i'))
        if t == 'bget':
            return self.bank_get(p, m.get('i'))
        if t == 'pact':
            return self.pet_interact(p, m.get('i'), str(m.get('a', '')), now)
        if t == 'use':
            return self.use_item(p, m.get('slot'), m.get('item'))
        if t == 'buy':
            return self.buy(p, m.get('item'), m.get('n', 1))
        if t == 'sell':
            return self.sell(p, m.get('slot'))
        if t == 'dlg':
            return self.npc_action(p, m.get('npc'), str(m.get('act', '')), m)
        if t == 'hstart':
            return self.hatch_start(p, m.get('slot'), now)
        if p.battle:   # 戰鬥中不能移動
            return
        p.idle_since = now
        if t == 'move':
            gx, gy = int(float(m['x'])), int(float(m['y']))
            p.clear_actions()
            p.path = self.find_path(int(p.x), int(p.y), gx, gy) or []
        elif t == 'dir':
            dx, dy = max(-1, min(1, int(m.get('dx', 0)))), max(-1, min(1, int(m.get('dy', 0))))
            l = math.hypot(dx, dy)
            p.dir = (dx / l, dy / l) if l else (0.0, 0.0)
            if l:
                p.clear_actions()
        elif t == 'npc':
            if m.get('id') in self.npc_by_id:
                p.clear_actions()
                p.npc = m['id']
        elif t == 'boss':
            if self.boss['alive']:
                p.clear_actions()
                p.boss_go = True
        elif t == 'bjoin':
            b = self.battles.get(m.get('b'))
            if b and not b.over and dist(p.x, p.y, b.cx, b.cy) <= 7:
                self.join_battle(b, p, now)

    def chat(self, p, msg, now):
        msg = str(msg).strip()[:100]
        if not msg or now - p.last_chat < 0.4:
            return
        p.last_chat = now
        if msg.startswith('/'):
            parts = msg.split(None, 2)
            cmd = parts[0].lower()
            if cmd in ('/w', '/密'):
                if len(parts) < 3:
                    return self.sys(p, '用法:/w 角色名稱 訊息')
                tgt = self.by_name.get(parts[1])
                if not tgt:
                    return self.sys(p, '%s 目前不在線上。' % parts[1])
                tgt.ws.send({'t': 'chat', 'ch': 'w', 'n': p.name, 'm': parts[2]})
                p.ws.send({'t': 'chat', 'ch': 'w', 'n': '→' + tgt.name, 'm': parts[2]})
            elif cmd == '/who':
                names = '、'.join('%s(Lv.%d %s)' % (q.name, q.lv, CLASSES[q.cls]['name']) for q in self.players.values())
                self.sys(p, '線上玩家 %d 人:%s' % (len(self.players), names))
            elif cmd in ('/help', '/?'):
                self.sys(p, '指令:/w 名稱 訊息 (密語)、/who (線上名單)')
            else:
                self.sys(p, '未知的指令,輸入 /help 查看說明。')
            return
        self.broadcast({'t': 'chat', 'ch': 'all', 'n': p.name, 'i': p.id, 'm': msg})

    # ---------- 寵物管理 ----------
    def get_pet(self, p, i):
        if isinstance(i, int) and 0 <= i < len(p.pets):
            return p.pets[i]
        return None

    def pet_set_active(self, p, i):
        pt = self.get_pet(p, i)
        if pt is None or p.battle:
            return
        p.active = i
        p.pets_dirty = True
        self.sys(p, '%s 成為出戰寵物。' % pt['n'])

    def pet_alloc(self, p, i, s, n):
        pt = self.get_pet(p, i)
        if pt is None or s not in (0, 1, 2, 3) or p.battle:
            return
        n = max(1, min(int(n), pt['pts']))
        if n <= 0 or pt['pts'] <= 0:
            return
        before = derive(pt['lv'], pt['st'])
        pt['st'][s] += n
        pt['pts'] -= n
        after = derive(pt['lv'], pt['st'])
        if pt['hp'] > 0:
            pt['hp'] += after['mhp'] - before['mhp']
        pt['mp'] += after['mmp'] - before['mmp']
        p.pets_dirty = True

    def pet_auto_alloc(self, p, i):
        pt = self.get_pet(p, i)
        if pt is None or pt['pts'] <= 0 or p.battle:
            return
        w = [x + 0.2 for x in SPECIES[pt['sp']]['pref']]
        while pt['pts'] > 0:
            self.pet_alloc(p, i, wpick(w), 1)

    def pet_rename(self, p, i, name):
        pt = self.get_pet(p, i)
        name = str(name).strip()[:8]
        if pt is None or not name or any(c in name for c in '<>&"\'/\\'):
            return
        pt['n'] = name
        p.pets_dirty = True

    def pet_release(self, p, i):
        pt = self.get_pet(p, i)
        if pt is None or p.battle:
            return
        if len(p.pets) <= 1:
            return self.sys(p, '你只剩這一隻寵物了,不能放生喔。')
        p.remove_pet(i)
        self.sys(p, '你放生了 %s。牠回頭看了你一眼,消失在草叢裡……' % pt['n'])

    def pet_sell(self, p, i):
        pt = self.get_pet(p, i)
        if pt is None or p.battle:
            return
        if not self.near_npc(p, 'hatcher'):
            return self.sys(p, '要賣寵物,請到孵化屋找葛莉絲婆婆。')
        if len(p.pets) <= 1:
            return self.sys(p, '你只剩這一隻寵物了,不能賣喔。')
        price = pet_price(pt)
        p.remove_pet(i)
        p.gold += price
        p.pets_dirty = p.inv_dirty = True
        self.sys(p, '把 %s 賣給了葛莉絲婆婆,獲得 %d 金幣。' % (pt['n'], price))

    # ---------- 寵物照顧 ----------
    def add_food(self, p, pt, delta):
        """改變飽食度,跨過「肚子餓」「餓昏」時通知主人"""
        old = pt['food']
        pt['food'] = round(clamp(old + delta), 4)
        if old >= CARE['hungry'] > pt['food'] and pt['food'] > 0:
            self.sys(p, '%s 肚子餓了……餵牠吃點東西吧。' % pt['n'])
            p.pets_dirty = True
        if old > 0 >= pt['food']:
            pt['bond'] = clamp(pt['bond'] + CARE['starve_bond'])
            self.sys(p, '%s 餓昏了!牠不肯戰鬥了,快餵牠吃東西!' % pt['n'], 'err')
            p.pets_dirty = True
        elif old <= 0 < pt['food']:
            p.pets_dirty = True

    def add_joy(self, pt, delta):
        pt['joy'] = round(clamp(pt['joy'] + delta), 4)

    def add_bond(self, pt, delta):
        pt['bond'] = round(clamp(pt['bond'] + delta), 4)

    def feed(self, p, i, item, now):
        pt = self.get_pet(p, i)
        if pt is None or item not in FOODS:
            return
        if p.battle:
            return self.sys(p, '戰鬥中不能餵食。')
        if self.count_item(p, item) <= 0:
            return self.sys(p, '你沒有%s了。' % FOODS[item]['name'])
        p.idle_since = now
        act = int(i == p.active)
        if pt['food'] >= CARE['full']:
            self.add_fx('pact', p.x, p.y, id=p.id, a='feed', r='full', act=act, sp=pt['sp'])
            return self.sys(p, '%s 已經吃得飽飽的,吃不下了。' % pt['n'])
        tst = taste(pt['sp'], item)
        fill, joy, bond = TASTE[tst]
        self.take_item(p, item)
        self.add_food(p, pt, fill)
        self.add_joy(pt, joy)
        self.add_bond(pt, bond)
        name = FOODS[item]['name']
        self.sys(p, {'love': '%s 吃了%s,開心得跳了起來!(最愛的食物)',
                     'like': '%s 把%s吃得津津有味。',
                     'ok': '%s 把%s吃掉了。',
                     'hate': '%s 皺著眉頭吃掉了%s……好像很討厭。'}[tst] % (pt['n'], name))
        self.add_fx('pact', p.x, p.y, id=p.id, a='feed', r=tst, f=item, act=act, sp=pt['sp'])
        p.pets_dirty = True

    def pet_interact(self, p, i, a, now):
        """互動動作:摸摸 / 玩耍 / 表演"""
        pt = self.get_pet(p, i)
        cfg = INTERACT.get(a)
        if pt is None or cfg is None or p.battle:
            return
        if cfg.get('need_bond') and pt['bond'] < cfg['need_bond']:
            return self.sys(p, '%s 跟你還不夠親(親密度要 %d),不肯表演。' % (pt['n'], cfg['need_bond']))
        if cfg.get('need_food') and pt['food'] < cfg['need_food']:
            return self.sys(p, '%s 肚子太餓了,沒力氣玩。' % pt['n'])
        cds = p.cd.setdefault(pt['uid'], {})
        if a == 'trick' and now < cds.get('anim', 0):
            return   # 表演動畫還沒做完
        gain = now >= cds.get(a, 0)
        p.idle_since = now
        if gain:
            cds[a] = now + cfg['cd']
            self.add_joy(pt, cfg['joy'])
            self.add_bond(pt, cfg['bond'])
            if cfg['food']:
                self.add_food(p, pt, cfg['food'])
            p.pets_dirty = True
        n = pt['n']
        if a == 'pet':
            self.sys(p, ('你摸了摸 %s,牠舒服地瞇起了眼睛。' if gain else '%s 被摸得有點不耐煩了,晚點再摸吧。') % n)
        elif a == 'play':
            self.sys(p, ('你陪 %s 玩了一會兒,牠玩得好開心!' if gain else '%s 玩累了,晚點再陪牠玩吧。') % n)
        else:
            cds['anim'] = now + 3
            self.sys(p, '%s 表演了「%s」!' % (n, SPECIES[pt['sp']]['trick'][0]))
        self.add_fx('pact', p.x, p.y, id=p.id, a=a, r='ok' if gain else 'cd', act=int(i == p.active), sp=pt['sp'])

    def run_away(self, p, pt):
        """溫和版離家出走:跑去寵物旅館賭氣"""
        if pt not in p.pets:
            return
        p.remove_pet(p.pets.index(pt))
        d = derive(pt['lv'], pt['st'])
        pt['hp'], pt['mp'] = d['mhp'], d['mmp']
        pt['sulk'] = True
        pt['food'] = max(pt['food'], float(CARE['sulk_food']))
        self.add_bond(pt, CARE['sulk_bond'])
        p.bank.append(pt)
        p.sulk.pop(pt['uid'], None)
        p.bank_dirty = True
        self.add_fx('pact', p.x, p.y, id=p.id, a='runaway', r='ok', act=1, sp=pt['sp'])
        self.sys(p, '%s 受不了了,賭氣跑去村裡的寵物旅館了!去找旅館的蘿絲帶牠回來吧。' % pt['n'], 'err')

    def care_tick(self, p, now, dt):
        """每秒一次:飽食度消耗、快樂值變化、離家出走、旅館裡的寵物恢復心情 (只有線上時才會跑)"""
        h = dt / 3600.0
        for i, pt in enumerate(list(p.pets)):
            self.add_food(p, pt, -(CARE['food_active'] if i == p.active else CARE['food_other']) * h)
            joy = -CARE['joy_decay'] * h
            if pt['food'] <= 0:
                joy -= CARE['joy_starve'] * h
            elif pt['food'] < CARE['hungry']:
                joy -= CARE['joy_hungry'] * h
            self.add_joy(pt, joy)
            uid = pt['uid']
            if pt['food'] <= 0 and pt['joy'] <= 0:
                if p.battle:   # 戰鬥中暫停計時 (不歸零)
                    continue
                s = p.sulk.get(uid, 0.0) + dt
                p.sulk[uid] = s
                if s - dt < CARE['sulk_warn'] <= s:
                    self.sys(p, '%s 好像快受不了了……再不理牠,牠可能會離家出走!' % pt['n'], 'err')
                if s >= CARE['sulk_leave']:
                    self.run_away(p, pt)
            else:
                p.sulk.pop(uid, None)
        for pt in p.bank:
            if pt['joy'] < 100:
                self.add_joy(pt, CARE['joy_bank'] * h)
        p.care_n += 1
        if p.care_n % 10 == 0:
            p.pets_dirty = True
            if p.bank:
                p.bank_dirty = True

    # ---------- 寵物旅館 ----------
    def bank_put(self, p, i):
        pt = self.get_pet(p, i)
        if pt is None or p.battle:
            return
        if not self.near_npc(p, 'keeper'):
            return self.sys(p, '要寄放寵物,請到村裡的寵物旅館找蘿絲。')
        if len(p.pets) <= 1:
            return self.sys(p, '身上至少要留一隻寵物喔。')
        if sum(1 for x in p.bank if not x.get('sulk')) >= CARE['bank_max']:
            return self.sys(p, '旅館已經住滿 %d 隻了。' % CARE['bank_max'])
        p.remove_pet(i)
        d = derive(pt['lv'], pt['st'])
        pt['hp'], pt['mp'] = d['mhp'], d['mmp']
        p.bank.append(pt)
        p.sulk.pop(pt['uid'], None)
        p.bank_dirty = True
        self.sys(p, '把 %s 寄放在寵物旅館了。' % pt['n'])

    def bank_get(self, p, i):
        if not isinstance(i, int) or not 0 <= i < len(p.bank) or p.battle:
            return
        if not self.near_npc(p, 'keeper'):
            return self.sys(p, '要領回寵物,請到村裡的寵物旅館找蘿絲。')
        if len(p.pets) >= PET_MAX:
            return self.sys(p, '身上已經有 %d 隻寵物了,先寄放一隻再領吧。' % PET_MAX)
        pt = p.bank.pop(i)
        p.pets.append(pt)
        p.pets_dirty = p.bank_dirty = True
        if pt.get('sulk'):
            pt['sulk'] = False
            if pt['joy'] < CARE['angry']:
                self.sys(p, '蘿絲:「%s 還在生悶氣呢……多摸摸牠、陪牠玩、餵牠愛吃的東西,心情就會好起來。」' % pt['n'])
            else:
                self.sys(p, '蘿絲:「%s 已經不生氣了,以後要好好照顧牠喔。」' % pt['n'])
        else:
            self.sys(p, '從寵物旅館領回了 %s。' % pt['n'])

    def pets_msg(self, p, now):
        idle = now - p.idle_since if not p.battle else 0
        out = []
        for pt in p.pets:
            v = pet_view(pt)
            v['mood'] = pet_mood(pt, idle)
            cds = p.cd.get(pt['uid'], {})
            v['cd'] = {a: max(0, int(cds.get(a, 0) - now)) for a in INTERACT}
            out.append(v)
        return {'t': 'pets', 'pets': out, 'act': p.active}

    def give_pet_exp(self, p, pt, amount):
        pt['exp'] += amount
        up = False
        while pt['lv'] < 99 and pt['exp'] >= exp_need(pt['lv']):
            pt['exp'] -= exp_need(pt['lv'])
            old = set(pet_skills(pt['sp'], pt['lv']))
            pt['lv'] += 1
            pt['pts'] += SPECIES[pt['sp']]['grow']
            d = derive(pt['lv'], pt['st'])
            pt['hp'], pt['mp'] = d['mhp'], d['mmp']
            self.add_joy(pt, CARE['levelup'][0])
            up = True
            self.sys(p, '%s 升到了 Lv.%d!獲得 %d 點能力點數。' % (pt['n'], pt['lv'], SPECIES[pt['sp']]['grow']))
            for sk in set(pet_skills(pt['sp'], pt['lv'])) - old:
                self.sys(p, '%s 學會了新技能「%s」!' % (pt['n'], PET_SKILLS[sk]['name']))
        p.pets_dirty = True
        return up

    def give_exp(self, p, amount):
        p.exp += amount
        up = False
        while p.lv < 99 and p.exp >= exp_need(p.lv):
            p.exp -= exp_need(p.lv)
            p.lv += 1
            up = True
        if up:
            p.recalc()
            p.hp, p.mp = p.mhp, p.mmp
            self.add_fx('lvl', p.x, p.y, id=p.id)
            self.sys(p, '恭喜!你的等級提升到 Lv.%d!' % p.lv)
            for sk in CLASSES[p.cls]['skills']:
                if sk['lv'] == p.lv:
                    self.sys(p, '你學會了新的輔助技能「%s」!' % sk['name'])
            if p.lv % 5 == 0:
                self.broadcast_sys('恭喜 %s 升到了 Lv.%d!' % (p.name, p.lv), 'ann')

    # ---------- 道具 ----------
    def add_item(self, p, item, n=1):
        for s in p.inv:
            if s['id'] == item and s['n'] + n <= 99:
                s['n'] += n
                p.inv_dirty = True
                return True
        if len(p.inv) >= INV_MAX:
            return False
        p.inv.append({'id': item, 'n': n})
        p.inv_dirty = True
        return True

    def count_item(self, p, item):
        return sum(s['n'] for s in p.inv if s['id'] == item)

    def take_item(self, p, item):
        for i, s in enumerate(p.inv):
            if s['id'] == item:
                s['n'] -= 1
                if s['n'] <= 0:
                    p.inv.pop(i)
                p.inv_dirty = True
                return True
        return False

    def use_item(self, p, slot, item):
        """在戰鬥外使用道具 (對出戰寵物)"""
        if p.battle:
            return self.sys(p, '戰鬥中請用主人的「道具」指令。')
        if item is not None:
            slot = next((i for i, s in enumerate(p.inv) if s['id'] == item), None)
            if slot is None:
                return self.sys(p, '%s 已經用完了!' % ITEMS.get(item, {}).get('name', '物品'))
        if not isinstance(slot, int) or not 0 <= slot < len(p.inv):
            return
        it = ITEMS[p.inv[slot]['id']]
        if it['type'] == 'food':
            if not p.pets:
                return self.sys(p, '你身上沒有寵物可以餵。')
            return self.feed(p, p.active, p.inv[slot]['id'], time.time())
        if it['type'] == 'egg':
            return self.sys(p, '蛋要拿到孵化屋找葛莉絲婆婆孵化喔。')
        if it['type'] != 'use':
            return self.sys(p, '%s 只能在戰鬥中使用。' % it['name'])
        if it.get('revive'):
            pt = next((x for x in p.pets if x['hp'] <= 0), None)
            if not pt:
                return self.sys(p, '沒有倒下的寵物。')
            pt['hp'] = max(1, int(derive(pt['lv'], pt['st'])['mhp'] * it['revive']))
        else:
            if not p.pets:
                return
            pt = p.pets[p.active]
            if pt['hp'] <= 0:
                return self.sys(p, '%s 已經倒下了,先用復活草吧。' % pt['n'])
            d = derive(pt['lv'], pt['st'])
            pt['hp'] = min(d['mhp'], pt['hp'] + it.get('hp', 0))
            pt['mp'] = min(d['mmp'], pt['mp'] + it.get('mp', 0))
        self.take_item(p, p.inv[slot]['id'])
        self.add_fx('heal', p.x, p.y, id=p.id, v=it.get('hp') or it.get('mp') or 0, mp=1 if it.get('mp') else 0)
        p.pets_dirty = True

    def near_npc(self, p, cls, r=4.0):
        return any(n['c'] == cls and dist(p.x, p.y, n['x'], n['y']) <= r for n in NPCS)

    def buy(self, p, item, n):
        if item in SHOP_ITEMS:
            seller = 'merchant'
        elif item in EGG_SHOP:
            seller = 'hatcher'
        else:
            return
        if not self.near_npc(p, seller):
            return self.sys(p, '離商人太遠了。')
        n = max(1, min(99, int(n)))
        cost = ITEMS[item]['price'] * n
        if p.gold < cost:
            return self.sys(p, '金幣不足!')
        if not self.add_item(p, item, n):
            return self.sys(p, '背包已經滿了!')
        p.gold -= cost
        p.inv_dirty = True
        self.sys(p, '購買了 %s ×%d,花費 %d 金幣。' % (ITEMS[item]['name'], n, cost))

    def sell(self, p, slot):
        if not isinstance(slot, int) or not 0 <= slot < len(p.inv):
            return
        if not (self.near_npc(p, 'merchant') or self.near_npc(p, 'hatcher')):
            return self.sys(p, '離商人太遠了。')
        s = p.inv[slot]
        price = ITEMS[s['id']]['price'] // 3
        self.take_item(p, s['id'])
        p.gold += price
        self.sys(p, '賣出了 %s,獲得 %d 金幣。' % (ITEMS[s['id']]['name'], price))

    # ---------- NPC ----------
    def open_npc(self, p, n):
        text, opts = NPC_DLG[n['c']]
        p.ws.send({'t': 'dlg', 'i': n['i'], 'n': n['n'], 'text': text, 'opts': opts})

    def npc_action(self, p, npc_id, act, m):
        n = self.npc_by_id.get(npc_id)
        if not n or dist(p.x, p.y, n['x'], n['y']) > 4:
            return self.sys(p, '距離太遠了。')
        c = n['c']
        if act == 'shop' and c == 'merchant':
            p.ws.send({'t': 'shop', 'i': n['i'], 'title': '道具商店', 'items': SHOP_ITEMS})
        elif act == 'eggs' and c == 'hatcher':
            p.ws.send({'t': 'shop', 'i': n['i'], 'title': '寵物蛋', 'items': EGG_SHOP})
        elif act == 'hatch' and c == 'hatcher':
            p.ws.send({'t': 'hatchui'})
        elif act == 'sellpet' and c == 'hatcher':
            p.ws.send({'t': 'petsell'})
        elif act == 'hint' and c == 'hatcher':
            text = '\n'.join(HATCH_HINTS.values()) + '\n\n蛋覺得舒服的時候,心跳會變得又穩又強。\n前 20 秒是預熱,慢慢找,不會影響結果喔。'
            p.ws.send({'t': 'dlg', 'i': n['i'], 'n': n['n'], 'text': text, 'opts': [['close', '謝謝婆婆']]})
        elif act == 'bank' and c == 'keeper':
            p.bank_dirty = True
            p.ws.send({'t': 'bankui'})
        elif act == 'bankinfo' and c == 'keeper':
            text = ('身上最多帶 %d 隻寵物,其他的可以寄放在旅館,最多 %d 隻。\n'
                    '住在這裡的孩子不會肚子餓,HP 和 MP 會補滿,心情也會慢慢變好。\n'
                    '要是有寵物賭氣跑來我這裡……別擔心,我會先餵牠吃點東西,你再來帶牠回去就好。'
                    % (PET_MAX, CARE['bank_max']))
            p.ws.send({'t': 'dlg', 'i': n['i'], 'n': n['n'], 'text': text, 'opts': [['close', '謝謝蘿絲']]})
        elif act == 'heal' and c == 'healer':
            p.hp, p.mp = p.mhp, p.mmp
            for pt in p.pets:
                d = derive(pt['lv'], pt['st'])
                pt['hp'], pt['mp'] = d['mhp'], d['mmp']
            p.pets_dirty = True
            self.add_fx('heal', p.x, p.y, id=p.id, v=p.mhp, big=1)
            self.sys(p, '修女瑪莉:願女神祝福你們!(你和所有寵物都完全恢復了)')
        elif act.startswith('tp:') and c == 'wizard':
            try:
                name, x, y, cost = TELEPORTS[int(act[3:])]
            except (ValueError, IndexError):
                return
            if p.gold < cost:
                return self.sys(p, '傳送師奧茲:金幣不夠喔,小朋友。')
            p.gold -= cost
            p.inv_dirty = True
            p.clear_actions()
            p.x, p.y = x, y
            p.steps = 0
            self.add_fx('tp', x, y, id=p.id)
            self.sys(p, '一陣光芒閃過……你被傳送到了%s。' % name)

    # ---------- 孵蛋 ----------
    def hatch_start(self, p, slot, now):
        if p.hatch:
            return self.sys(p, '孵蛋器裡已經有一顆蛋了。')
        if not self.near_npc(p, 'hatcher'):
            return self.sys(p, '請到孵化屋找葛莉絲婆婆孵蛋。')
        if not isinstance(slot, int) or not 0 <= slot < len(p.inv) or ITEMS[p.inv[slot]['id']]['type'] != 'egg':
            return
        if len(p.pets) >= PET_MAX:
            return self.sys(p, '身上的寵物已經有 %d 隻了,先寄放到寵物旅館、賣掉或放生一隻再來孵吧。' % PET_MAX)
        egg = p.inv[slot]['id']
        self.take_item(p, egg)
        p.hatch = {'egg': egg, 'sp': ITEMS[egg]['sp'], 'start': now, 'kt': 50.0, 'kh': 50.0,
                   'ot': random.uniform(-12, 12), 'oh': random.uniform(-12, 12), 'vt': 0.0, 'vh': 0.0,
                   'sum': 0.0, 'n': 0, 'send': 0.0}
        self.sys(p, '把%s放進孵蛋器了。調整溫度和濕度,讓蛋覺得舒服吧!' % ITEMS[egg]['name'])

    def hatch_tick(self, p, now, dt):
        h = p.hatch
        for o, v in (('ot', 'vt'), ('oh', 'vh')):   # 環境溫濕度會慢慢飄移
            h[v] = max(-2.5, min(2.5, h[v] + random.uniform(-3, 3) * dt))
            h[o] += h[v] * dt
            if abs(h[o]) > 30:
                h[o] = max(-30, min(30, h[o]))
                h[v] = -h[v] * 0.5
        at = max(0.0, min(100.0, h['kt'] + h['ot']))
        ah = max(0.0, min(100.0, h['kh'] + h['oh']))
        egg = SPECIES[h['sp']]['egg']
        d = math.hypot(at - egg['temp'], ah - egg['hum'])
        c = 1.0 if d <= 3 else max(0.0, 1 - (d - 3) / 25.0)
        el = now - h['start']
        if el >= HATCH_WARMUP:
            h['sum'] += c
            h['n'] += 1
        if now >= h['send']:
            h['send'] = now + 0.2
            p.ws.send({'t': 'hatch', 'sp': h['sp'], 'el': round(el, 1), 'at': round(at, 1), 'ah': round(ah, 1),
                       'kt': round(h['kt'], 1), 'kh': round(h['kh'], 1), 'c': round(c, 2)})
        if el >= HATCH_TIME:
            avg = h['sum'] / h['n'] if h['n'] else c
            q = max(0, min(12, int(round(12 * avg ** 1.5))))
            pt = new_pet(h['sp'], 1, q, start='hatch')
            p.hatch = None
            p.pets.append(pt)
            p.pets_dirty = True
            p.ws.send({'t': 'hatched', 'pet': pet_view(pt)})
            self.add_fx('lvl', p.x, p.y, id=p.id, hatch=1)
            self.sys(p, '蛋殼裂開了……孵出了 %s!天生素質 %d 點 (%s)' % (pt['n'], q, '★' * stars(q)))
            if q >= 12:
                self.broadcast_sys('%s 孵出了 12 點的極品%s!葛莉絲婆婆都看呆了!' % (p.name, pt['n']), 'ann')

    # ============================================================
    #  戰鬥
    # ============================================================
    def zone_at(self, x, y):
        d = dist(x, y, *CENTER)
        for z in ZONES:
            if z['d'][0] <= d < z['d'][1]:
                return z
        return ZONES[-1]

    def encounter_check(self, p, moved, now):
        if in_town(p.x, p.y, 1.0) or p.hatch:
            return
        tile = self.tile_at(p.x, p.y)
        if tile == T_ASH or p.alive_pet() is None:
            return
        rate = ENCOUNTER_RATE * CLASSES[p.cls]['enc'] * (ROAD_ENCOUNTER if tile in (T_SAND, T_BRIDGE) else 1.0)
        p.enc_dist += moved
        while p.enc_dist >= 1.0:
            p.enc_dist -= 1.0
            p.steps += 1
            if p.steps >= ENCOUNTER_MIN_STEPS and random.random() < rate:
                self.start_encounter(p, now)
                return

    def wild_unit(self, sp, lv, rare=False):
        s = SPECIES[sp]
        q = wpick(WILD_QUALITY_WEIGHTS)
        st = list(s['base'])
        w = [x + 0.2 for x in s['pref']]
        for _ in range(q + s['grow'] * (lv - 1)):
            st[wpick(w)] += 1
        d = derive(lv, st)
        d['mhp'] = int(d['mhp'] * WILD_POWER)
        d['atk'] = int(d['atk'] * WILD_POWER)
        d['matk'] = int(d['matk'] * WILD_POWER)
        d['spd'] *= 0.9
        u = Unit(self.nid(), 1, 'm', s['name'], lv)
        u.sp, u.el, u.q = sp, s['el'], q
        u.set_stats(d)
        u.hp, u.mp = u.mhp, u.mmp
        u.skills = pet_skills(sp, lv)
        u.exp = int((6 + lv * 4) * (2 if rare else 1))
        u.gold = lv * 2 + random.randint(1, 5)
        u.bar = random.uniform(0, 45)
        return u

    def owner_unit(self, p):
        u = Unit(self.nid(), 0, 'o', p.name, p.lv)
        u.cls, u.pid = p.cls, p.id
        u.mhp, u.mmp, u.hp, u.mp = p.mhp, p.mmp, p.hp, p.mp
        u.spd = CLASSES[p.cls]['spd']
        u.bar = random.uniform(20, 40)
        return u

    def pet_unit(self, p, idx):
        pt = p.pets[idx]
        u = Unit(self.nid(), 0, 'p', pt['n'], pt['lv'])
        u.sp, u.el, u.pid, u.pet, u.q = pt['sp'], SPECIES[pt['sp']]['el'], p.id, pt, pt['q']
        u.set_stats(derive(pt['lv'], pt['st']))
        if pt['food'] < CARE['hungry']:   # 肚子餓:能力下降
            k = CARE['hungry_mult']
            u.atk, u.matk, u.df, u.mdf = int(u.atk * k), int(u.matk * k), int(u.df * k), int(u.mdf * k)
        u.hp, u.mp = min(pt['hp'], u.mhp), min(pt['mp'], u.mmp)
        u.skills = pet_skills(pt['sp'], pt['lv'])
        u.bar = random.uniform(35, 65)
        u.sync = pt['sync']
        return u

    def boss_unit(self, nplayers):
        u = Unit(self.nid(), 1, 'm', BOSS['name'], BOSS['lv'])
        u.sp, u.el, u.boss = 'dragon', BOSS['el'], True
        u.mhp = BOSS['hp'] + BOSS['hp_per_player'] * max(0, nplayers - 1)
        u.mmp = BOSS['mp']
        u.atk, u.matk, u.df, u.mdf = BOSS['atk'], BOSS['matk'], BOSS['def'], BOSS['mdef']
        u.spd, u.eva = BOSS['spd'], BOSS['eva']
        u.hp, u.mp = u.mhp, u.mmp
        u.exp, u.gold = BOSS['exp'], BOSS['gold']
        return u

    def new_battle(self, cx, cy, boss=False):
        b = Battle(self.nid(), cx, cy, boss)
        self.battles[b.id] = b
        return b

    def add_player(self, b, p, now):
        ou = b.add(self.owner_unit(p))
        b.ou[p.id] = ou.id
        idx = p.alive_pet()
        if idx is not None:
            p.active = idx
            pu = b.add(self.pet_unit(p, idx))
            b.pu[p.id] = pu.id
            b.fought.setdefault(p.id, set()).add(p.pets[idx]['uid'])
        b.pids.append(p.id)
        self.restack(b)
        p.battle = b.id
        p.btarget = 0
        p.path, p.dir, p.moving = [], (0.0, 0.0), False
        p.npc, p.boss_go = None, False
        p.pets_dirty = True

    def restack(self, b):
        for row, pid in enumerate(b.pids):
            for uid in (b.ou.get(pid), b.pu.get(pid)):
                if uid in b.units:
                    b.units[uid].row = row
        for row, u in enumerate(x for x in b.units.values() if x.side == 1):
            u.row = row

    def start_encounter(self, p, now):
        z = self.zone_at(p.x, p.y)
        n = 1 + wpick([6, 3, 1.2, 0.5][:z['max']])
        b = self.new_battle(p.x, p.y)
        self.add_player(b, p, now)
        rare_sp, chance, rlo, rhi = z['rare']
        rare = random.random() < chance
        for i in range(n):
            if rare and i == 0:
                u = self.wild_unit(rare_sp, random.randint(rlo, rhi), True)
            else:
                sp, lo, hi, _ = z['mobs'][wpick([m[3] for m in z['mobs']])]
                u = self.wild_unit(sp, random.randint(lo, hi))
            b.add(u)
        self.restack(b)
        self.bfx(b, 'bstart')
        if rare:
            self.sys(p, '★ 稀有寵物「%s」出現了!快用封印卡收服牠!' % SPECIES[rare_sp]['name'], 'ann')

    def start_boss(self, p, now):
        bs = self.boss
        if bs['battle'] in self.battles:
            return self.join_battle(self.battles[bs['battle']], p, now)
        if p.alive_pet() is None:
            return self.sys(p, '你的寵物都倒下了,沒辦法挑戰炎龍。')
        b = self.new_battle(bs['x'] - 1.5, bs['y'], boss=True)
        self.add_player(b, p, now)
        b.add(self.boss_unit(1))
        self.restack(b)
        bs['battle'] = b.id
        self.bfx(b, 'bstart')
        self.broadcast_sys('%s 向炎龍發起了挑戰!' % p.name, 'ann')

    def join_battle(self, b, p, now):
        if p.battle or b.over:
            return
        if len(b.pids) >= PARTY_MAX:
            return self.sys(p, '這場戰鬥已經滿 %d 人了。' % PARTY_MAX)
        if p.alive_pet() is None:
            return self.sys(p, '你的寵物都倒下了,沒辦法加入戰鬥。')
        self.add_player(b, p, now)
        if b.boss:   # 炎龍的血量依人數增加
            for u in b.alive(1):
                extra = BOSS['hp_per_player']
                u.mhp += extra
                u.hp += extra
        p.x, p.y = b.cx, b.cy
        self.bfx(b, 'join', id=b.ou[p.id])
        for q in b.pids:
            if q != p.id and q in self.players:
                self.sys(self.players[q], '%s 加入了戰鬥!' % p.name)

    def sync_pet(self, b, p):
        """把出戰寵物在戰鬥中的 HP/MP 寫回寵物資料"""
        u = b.units.get(b.pu.get(p.id))
        if u and u.pet is not None:
            u.pet['hp'] = max(0, int(u.hp)) if u.alive else 0
            u.pet['mp'] = max(0, int(u.mp))
            u.pet['sync'] = round(u.sync, 2)

    def battle_care(self, b, p, result):
        """戰鬥結束時的照顧數值:上場過的寵物消耗飽食度,打贏開心、打輸難過"""
        fought = b.fought.get(p.id, ())
        for pt in p.pets:
            if pt['uid'] not in fought:
                continue
            self.add_food(p, pt, -CARE['food_battle'])
            if result in ('win', 'lose'):
                joy, bond = CARE[result]
                if result == 'lose' or pt['hp'] > 0:
                    self.add_joy(pt, joy)
                    self.add_bond(pt, bond)
        p.pets_dirty = True
        p.idle_since = time.time()

    def leave_battle(self, b, p, now):
        self.sync_pet(b, p)
        self.battle_care(b, p, 'flee')
        ou = b.units.get(b.ou.get(p.id))
        if ou:
            p.hp, p.mp = max(1, int(ou.hp)), max(0, int(ou.mp))
        for uid in (b.ou.pop(p.id, None), b.pu.pop(p.id, None)):
            b.units.pop(uid, None)
        if p.id in b.pids:
            b.pids.remove(p.id)
        p.battle = None
        p.steps = 0
        p.pets_dirty = True
        if not b.pids:
            self.close_battle(b)
        else:
            self.restack(b)

    def close_battle(self, b):
        b.over = True
        self.battles.pop(b.id, None)
        if b.boss and self.boss['battle'] == b.id:
            self.boss['battle'] = None

    # ----- 傷害計算 -----
    def hit(self, b, src, tgt, kind, mult, now, el=None, pierce=False):
        if not tgt.alive:
            return 0
        if kind == 'phys' and random.random() < tgt.eva:
            self.bfx(b, 'hit', id=tgt.id, v=0, s=src.id)
            return 0
        guard_def = smod(tgt, 'defup', 1.4) * smod(tgt, 'defdown', 0.7) * smod(tgt, 'protect', CARE['guard_def'])
        if kind == 'phys':
            atk = src.atk * smod(src, 'atkup', 1.3) * smod(src, 'atkdown', 0.8)
            df = 0 if pierce else tgt.df * guard_def
        else:
            atk = src.matk * smod(src, 'matkup', 1.35) * smod(src, 'atkdown', 0.8)
            df = tgt.mdf * guard_def
            el = el or src.el
        dmg = atk * mult * random.uniform(0.9, 1.1) - df * 0.7
        crit = kind == 'phys' and random.random() < 0.08
        if crit:
            dmg *= 1.5
        em = elem_mult(el, tgt.el)
        dmg *= em
        if el and b.weather:
            dmg *= WEATHER[b.weather].get(el, 1.0)
        if 'guard' in tgt.status:
            dmg *= 0.5
        dmg = max(1, int(dmg))
        self.bfx(b, 'hit', id=tgt.id, v=dmg, c=int(crit), s=src.id, e=1 if em > 1 else -1 if em < 1 else 0)
        self.damage(b, tgt, dmg, now)
        return dmg

    def damage(self, b, tgt, dmg, now):
        if tgt.shield > 0:
            ab = min(tgt.shield, dmg)
            tgt.shield -= ab
            dmg -= ab
            if tgt.shield <= 0:
                tgt.status.pop('shield', None)
        tgt.hp -= dmg
        tgt.status.pop('sleep', None)
        if tgt.kind == 'p' and dmg > 0:      # 寵物受傷,主人也會間接受傷 (親密度越高越少;護主時不會)
            self.add_sync(tgt, CARE['sync_hit'])
            ou = b.units.get(b.ou.get(tgt.pid))
            bond = tgt.pet['bond'] if tgt.pet is not None else 0
            link = 0 if 'protect' in tgt.status else int(dmg * link_ratio(bond))
            if ou and ou.alive and link > 0:
                ou.hp -= link
                self.bfx(b, 'hit', id=ou.id, v=link, link=1)
                if ou.hp <= 0:
                    self.ko(b, ou, now)
        if tgt.hp <= 0 and tgt.alive:
            self.ko(b, tgt, now)

    def heal_unit(self, b, u, amount):
        amount = max(1, int(amount))
        u.hp = min(u.mhp, u.hp + amount)
        self.bfx(b, 'heal', id=u.id, v=amount)

    def ko(self, b, u, now):
        u.hp = 0
        u.alive = False
        u.ready_at = None
        u.bar = 0
        u.status = {}
        u.shield = 0
        self.bfx(b, 'ko', id=u.id)
        if u.kind == 'm':
            b.exp += u.exp
            b.gold += u.gold
            if u.boss:
                b.loot.append('egg_drake')
            else:
                for item, chance in (('red_potion', 0.1), ('seal_card', 0.06), ('blue_potion', 0.04), ('revive_herb', 0.02)):
                    if random.random() < chance:
                        b.loot.append(item)
                if random.random() < CARE['food_drop']:   # 掉落牠最愛的食物
                    love = SPECIES[u.sp].get('love')
                    b.loot.append(random.choice(list(FOODS)) if love == '*' or love not in FOODS else love)
            b.units.pop(u.id, None)
        elif u.kind == 'p':
            u.surge = False
            if u.pet is not None:
                u.pet['hp'] = 0
                joy, bond = CARE['ko']
                self.add_joy(u.pet, joy)
                self.add_bond(u.pet, bond)
            p = self.players.get(u.pid)
            if p:
                self.sys(p, '%s 倒下了!快換一隻寵物,或用復活草救牠!' % u.name, 'err')
        elif u.kind == 'o':
            p = self.players.get(u.pid)
            pu = b.units.get(b.pu.get(u.pid))
            if p:
                self.sync_pet(b, p)
                self.sys(p, '你倒下了……寵物們退出了戰鬥。', 'err')
            if pu:
                b.units.pop(pu.id, None)
                b.pu.pop(u.pid, None)

    def end_turn(self, u):
        u.bar = 0
        u.ready_at = None
        u.acts += 1
        if u.kind == 'p':
            self.add_sync(u, CARE['sync_act'])

    def can_act(self, u):
        return u is not None and u.alive and u.ready_at is not None and 'sleep' not in u.status

    # ----- 親密度:默契、助攻、不聽指令 -----
    def add_sync(self, u, base):
        """默契量表:親密度 40 以上才會累積"""
        if u.pet is None or u.pet['bond'] < CARE['sync_bond'] or u.sync >= 100:
            return
        u.sync = min(100.0, u.sync + sync_gain(base, u.pet['bond']))

    def take_surge(self, u):
        """助攻發動後的下一招:回傳威力倍率"""
        if u.surge:
            u.surge = False
            return CARE['sync_power']
        return 1.0

    def assist(self, b, p, now):
        """助攻 (主人的免費行動):默契滿了,寵物立刻行動,下一招威力 ×1.5、不耗 MP"""
        ou = b.units.get(b.ou.get(p.id))
        u = b.units.get(b.pu.get(p.id))
        if not ou or not ou.alive or not u or not u.alive or u.pet is None:
            return
        if u.pet['bond'] < CARE['sync_bond']:
            return self.sys(p, '親密度要 %d 以上才能助攻。' % CARE['sync_bond'])
        if u.sync < 100 or 'sleep' in u.status or u.surge:
            return
        u.sync = 0.0
        u.surge = True
        u.bar = 100
        if u.ready_at is None:
            u.ready_at = now
        self.bfx(b, 'assist', id=u.id, o=ou.id)

    def pet_disobeys(self, b, u, p, now):
        """心情不好的寵物可能不聽指令:一半發呆、一半自己亂打"""
        pt = u.pet
        if pt is None or u.surge:
            return False
        ch = disobey_chance(pt['joy'], pt['bond'])
        if ch <= 0 or random.random() >= ch:
            return False
        foes = b.alive(1 - u.side)
        self.bfx(b, 'disobey', id=u.id)
        if foes and random.random() < 0.5:
            self.do_attack(b, u, random.choice(foes), now)
        else:
            u.status.pop('guard', None)
            self.bfx(b, 'act', s=u.id, t=0, w='sulk', n='哼!', ty='status')
            self.end_turn(u)
        self.sys(p, '%s 心情不好,不聽指令!' % u.name)
        return True

    def guard_check(self, b, now):
        """護主姿態:主人 HP 低於 30% 時,親密度夠高的寵物擋到主人前面"""
        for pid in b.pids:
            ou, u = b.units.get(b.ou.get(pid)), b.units.get(b.pu.get(pid))
            if not u or not u.alive or u.pet is None:
                continue
            on = 'protect' in u.status
            if not on and ou and ou.alive and u.pet['bond'] >= CARE['guard_bond'] and ou.hp < ou.mhp * CARE['guard_enter']:
                u.status['protect'] = now + 99999
                self.bfx(b, 'act', s=u.id, t=ou.id, w='protect', n='挺身護主!', ty='status')
                self.bfx(b, 'st', id=u.id, st='protect', ok=1)
            elif on and (not ou or not ou.alive or ou.hp >= ou.mhp * CARE['guard_leave']):
                u.status.pop('protect', None)

    # ----- 寵物 / 敵人的行動 -----
    def do_attack(self, b, u, tgt, now):
        u.status.pop('guard', None)
        power = self.take_surge(u)
        self.bfx(b, 'act', s=u.id, t=tgt.id, w='melee', n='' if power == 1 else '全力一擊')
        self.hit(b, u, tgt, 'phys', 1.0 * power, now)
        self.end_turn(u)

    def do_skill(self, b, u, sk, tgt, now):
        s = PET_SKILLS[sk]
        u.status.pop('guard', None)
        power = self.take_surge(u)
        if power == 1:
            u.mp -= s['mp']
        side_foe = 1 - u.side
        self.bfx(b, 'act', s=u.id, t=tgt.id if tgt else 0, w=s['fx'], n=s['name'], ty=s['type'])
        if s['type'] == 'heal':
            self.heal_unit(b, tgt, (tgt.mhp * s['mult'] + u.matk * 0.5) * power)
        elif s['type'] == 'status':
            key, dur = s['status']
            ok = random.random() < min(1.0, s.get('chance', 1.0) * power) and not tgt.boss
            if ok:
                tgt.status[key] = now + dur
            self.bfx(b, 'st', id=tgt.id, st=key, ok=int(ok))
        elif s['target'] == 'enemies':
            for t in b.alive(side_foe):
                self.hit(b, u, t, s['type'], s['mult'] * power, now, s.get('el'))
        else:
            for _ in range(s.get('hits', 1)):
                if not tgt.alive:
                    break
                d = self.hit(b, u, tgt, s['type'], s['mult'] * power, now, s.get('el'), s.get('pierce', False))
                if s.get('drain') and d:
                    self.heal_unit(b, u, d * s['drain'])
            if s.get('status') and tgt.alive and random.random() < 0.6:
                key, dur = s['status']
                tgt.status[key] = now + dur
                if key == 'poison':
                    tgt.next_poison = now + 2
                self.bfx(b, 'st', id=tgt.id, st=key, ok=1)
        self.end_turn(u)

    def pick_foe(self, b, u):
        foes = b.alive(1 - u.side)
        if not foes:
            return None
        if u.side == 1:   # 敵人優先攻擊寵物
            pets = [x for x in foes if x.kind == 'p']
            return random.choice(pets or foes)
        p = self.players.get(u.pid)
        tg = b.units.get(p.btarget) if p else None
        if tg and tg.alive and tg.side == 1:
            return tg
        return random.choice(foes)

    def ai_act(self, b, u, now, smart=True):
        if u.boss:
            return self.boss_act(b, u, now)
        tgt = self.pick_foe(b, u)
        if tgt is None:
            return
        if smart and u.skills:
            usable = [s for s in u.skills if PET_SKILLS[s]['mp'] <= u.mp]
            heal = [s for s in usable if PET_SKILLS[s]['type'] == 'heal']
            hurt = [x for x in b.alive(u.side) if x.kind != 'o' and x.hp < x.mhp * 0.5]
            if heal and hurt:
                return self.do_skill(b, u, heal[0], min(hurt, key=lambda x: x.hp / x.mhp), now)
            usable = [s for s in usable if PET_SKILLS[s]['type'] != 'heal']
            if usable and random.random() < (0.55 if u.side == 0 else 0.35):
                return self.do_skill(b, u, random.choice(usable), tgt, now)
        self.do_attack(b, u, tgt, now)

    def boss_act(self, b, u, now):
        if u.acts % 3 == 2:
            self.bfx(b, 'act', s=u.id, t=0, w='breath', n='烈焰吐息', ty='mag')
            for t in b.alive(0):
                if t.kind == 'p':
                    self.hit(b, u, t, 'mag', 1.0, now, 'fire')
            self.end_turn(u)
        else:
            tgt = self.pick_foe(b, u)
            if tgt:
                self.bfx(b, 'act', s=u.id, t=tgt.id, w='bite', n='撕咬' if u.acts % 3 else '', ty='phys')
                self.hit(b, u, tgt, 'phys', 1.3, now)
            self.end_turn(u)
        if u.hp < u.mhp * 0.3 and 'haste' not in u.status:
            u.status['haste'] = now + 999
            self.bfx(b, 'act', s=u.id, t=0, w='roar', n='炎龍暴怒了!', ty='status')

    # ----- 玩家下指令 -----
    def battle_cmd(self, p, m, now):
        b = self.battles.get(p.battle)
        if not b or b.over:
            return
        who, a = m.get('u'), m.get('a')
        tg = b.units.get(m.get('tg'))
        if who == 'o' and a == 'assist':   # 助攻不用等主人的時間棒
            self.assist(b, p, now)
            return
        if who == 'p':
            u = b.units.get(b.pu.get(p.id))
            if not self.can_act(u):
                return
            if a == 'skill':
                sk = m.get('s')
                if sk not in u.skills:
                    return
                if u.mp < PET_SKILLS[sk]['mp'] and not u.surge:
                    return self.sys(p, 'MP 不足!')
            if a in ('atk', 'skill', 'def') and self.pet_disobeys(b, u, p, now):
                return self.check_end(b, now)
            foe = tg if tg and tg.alive and tg.side == 1 else self.pick_foe(b, u)
            if a == 'atk' and foe:
                self.do_attack(b, u, foe, now)
            elif a == 'skill':
                sk = m.get('s')
                s = PET_SKILLS[sk]
                if s['target'] == 'ally':
                    t = tg if tg and tg.alive and tg.side == 0 and tg.kind == 'p' else u
                    self.do_skill(b, u, sk, t, now)
                elif foe:
                    self.do_skill(b, u, sk, foe, now)
            elif a == 'def':
                u.status['guard'] = now + 999
                self.bfx(b, 'act', s=u.id, t=0, w='guard', n='防禦', ty='status')
                self.end_turn(u)
        elif who == 'o':
            u = b.units.get(b.ou.get(p.id))
            if not self.can_act(u):
                return
            if a == 'oskill':
                self.owner_skill(b, p, u, m.get('s'), tg, now)
            elif a == 'item':
                self.battle_item(b, p, u, m.get('item'), tg, now)
            elif a == 'cap':
                self.capture(b, p, u, tg, now)
            elif a == 'swap':
                self.swap_pet(b, p, u, m.get('i'), now)
            elif a == 'flee':
                self.flee(b, p, u, now)
            elif a == 'wait':
                self.end_turn(u)
        self.check_end(b, now)

    def ally_pet_target(self, b, p, tg, need_alive=True):
        if tg and tg.side == 0 and tg.kind == 'p' and (tg.alive or not need_alive):
            return tg
        own = b.units.get(b.pu.get(p.id))
        if own and (own.alive or not need_alive):
            return own
        return None

    def owner_skill(self, b, p, u, idx, tg, now):
        skills = CLASSES[p.cls]['skills']
        if not isinstance(idx, int) or not 0 <= idx < len(skills):
            return
        sk = skills[idx]
        if p.lv < sk['lv']:
            return self.sys(p, '%s 需要 Lv.%d 才能使用。' % (sk['name'], sk['lv']))
        if u.mp < sk['mp']:
            return self.sys(p, 'MP 不足!')
        eff, tgt = sk['eff'], None
        if sk['target'] == 'ally':
            tgt = self.ally_pet_target(b, p, tg, need_alive=(eff != 'revive'))
            if eff == 'revive' and tgt and tgt.alive:
                tgt = next((x for x in b.units.values() if x.side == 0 and x.kind == 'p' and not x.alive), None)
            if tgt is None:
                return self.sys(p, '沒有可以施放的對象。')
        elif sk['target'] == 'enemy':
            tgt = tg if tg and tg.alive and tg.side == 1 else self.pick_foe(b, b.units.get(b.pu.get(p.id)) or u)
            if tgt is None:
                return
        u.mp -= sk['mp']
        self.bfx(b, 'act', s=u.id, t=tgt.id if tgt else 0, w='owner_' + eff, n=sk['name'], ty='owner')

        def boost(t):
            """助攻加成:用在自己的寵物身上,效果隨親密度增強"""
            if t is not None and t.kind == 'p' and t.pid == p.id and t.pet is not None:
                k = assist_mult(t.pet['bond'])
                if k > 1.01:
                    self.bfx(b, 'boost', id=t.id, v=int(round((k - 1) * 100)))
                return k
            return 1.0
        if eff == 'buff':
            tgt.status[sk['st']] = now + sk['dur']
            tgt.stmul[sk['st']] = boost(tgt)
            self.bfx(b, 'st', id=tgt.id, st=sk['st'], ok=1)
        elif eff == 'debuff':
            for t in (b.alive(1) if sk['target'] == 'enemies' else [tgt]):
                t.status[sk['st']] = now + sk['dur']
                if sk.get('val'):
                    t.bar = max(0, t.bar + sk['val'])
                    if t.ready_at is not None and t.bar < 100:
                        t.ready_at = None
                self.bfx(b, 'st', id=t.id, st=sk['st'], ok=1)
        elif eff == 'bar':
            if tgt.ready_at is None:
                tgt.bar = min(99.9, tgt.bar + sk['val'] * boost(tgt))
            self.bfx(b, 'st', id=tgt.id, st='haste', ok=1)
        elif eff == 'heal':
            self.heal_unit(b, tgt, (tgt.mhp * sk['val'] + p.lv * 4) * boost(tgt))
        elif eff == 'shield':
            tgt.shield = int(tgt.mhp * sk['val'] * boost(tgt))
            tgt.status['shield'] = now + 999
            self.bfx(b, 'st', id=tgt.id, st='shield', ok=1)
        elif eff == 'revive':
            if tgt.alive:
                return self.end_turn(u)
            self.revive(b, tgt, min(1.0, sk['val'] * boost(tgt)))
        elif eff == 'weather':
            b.weather, b.weather_until = sk['val'], now + sk['dur']
            self.bfx(b, 'weather', w=sk['val'])
        elif eff == 'mpall':
            for t in b.alive(0):
                if t.kind == 'p':
                    gain = int((sk['val'] + p.lv * 2) * boost(t))
                    t.mp = min(t.mmp, t.mp + gain)
                    self.bfx(b, 'heal', id=t.id, v=gain, mp=1)
        elif eff == 'sleep':
            ok = random.random() < sk['val'] and not tgt.boss
            if ok:
                tgt.status['sleep'] = now + sk['dur']
            self.bfx(b, 'st', id=tgt.id, st='sleep', ok=int(ok))
        elif eff == 'hasteall':
            for t in b.alive(0):
                if t.kind == 'p':
                    t.status['haste'] = now + sk['dur']
                    t.stmul['haste'] = boost(t)
                    self.bfx(b, 'st', id=t.id, st='haste', ok=1)
        self.end_turn(u)

    def revive(self, b, t, ratio):
        t.alive = True
        t.hp = max(1, int(t.mhp * ratio))
        t.bar = 0
        t.ready_at = None
        if t.pet is not None:
            t.pet['hp'] = t.hp
        self.bfx(b, 'revive', id=t.id, v=t.hp)

    def battle_item(self, b, p, u, item, tg, now):
        it = ITEMS.get(item)
        if not it or it['type'] != 'use' or self.count_item(p, item) <= 0:
            return self.sys(p, '沒有這個道具了。')
        if it.get('revive'):
            t = tg if tg and tg.side == 0 and tg.kind == 'p' and not tg.alive else \
                next((x for x in b.units.values() if x.side == 0 and x.kind == 'p' and not x.alive), None)
            if not t:
                return self.sys(p, '沒有倒下的寵物。')
            self.take_item(p, item)
            self.bfx(b, 'act', s=u.id, t=t.id, w='owner_item', n=it['name'], ty='owner')
            self.revive(b, t, it['revive'])
        else:
            t = self.ally_pet_target(b, p, tg)
            if not t:
                return self.sys(p, '沒有可以使用的對象。')
            self.take_item(p, item)
            self.bfx(b, 'act', s=u.id, t=t.id, w='owner_item', n=it['name'], ty='owner')
            if it.get('hp'):
                self.heal_unit(b, t, it['hp'])
            if it.get('mp'):
                t.mp = min(t.mmp, t.mp + it['mp'])
                self.bfx(b, 'heal', id=t.id, v=it['mp'], mp=1)
        self.end_turn(u)

    def capture(self, b, p, u, tg, now):
        if not tg or not tg.alive or tg.side != 1:
            return self.sys(p, '請先點選要捕捉的敵人。')
        if tg.boss or not SPECIES.get(tg.sp, {}).get('cap'):
            return self.sys(p, '%s 太強大了,無法封印!' % tg.name)
        if len(p.pets) >= PET_MAX:
            return self.sys(p, '身上的寵物已經有 %d 隻了,沒有空的封印卡欄位(可以寄放到村裡的寵物旅館)。' % PET_MAX)
        if not self.take_item(p, 'seal_card'):
            return self.sys(p, '你沒有封印卡了!')
        chance = SPECIES[tg.sp]['cap'] * (1.15 - tg.hp / tg.mhp) * CLASSES[p.cls]['cap']
        if tg.lv > p.lv:
            chance *= max(0.3, 1 - (tg.lv - p.lv) * 0.08)
        if 'sleep' in tg.status:
            chance *= 1.3
        chance = max(0.03, min(0.95, chance))
        ok = random.random() < chance
        self.bfx(b, 'act', s=u.id, t=tg.id, w='owner_seal', n='封印卡', ty='owner')
        self.bfx(b, 'cap', s=u.id, id=tg.id, ok=int(ok), pct=int(chance * 100))
        if ok:
            pt = new_pet(tg.sp, tg.lv, tg.q, start='wild')
            p.pets.append(pt)
            p.pets_dirty = True
            b.exp += tg.exp // 2
            b.units.pop(tg.id, None)
            self.sys(p, '封印成功!收服了 Lv.%d %s,天生素質 %d 點 (%s)' % (pt['lv'], pt['n'], pt['q'], '★' * stars(pt['q'])))
            if pt['q'] >= 11:
                self.broadcast_sys('%s 抓到了天生素質 %d 點的極品%s!' % (p.name, pt['q'], pt['n']), 'ann')
        else:
            self.sys(p, '封印失敗了……(成功率 %d%%)' % int(chance * 100))
        self.end_turn(u)

    def swap_pet(self, b, p, u, idx, now):
        if not isinstance(idx, int) or not 0 <= idx < len(p.pets):
            return
        old = b.units.get(b.pu.get(p.id))
        if old and old.pet is p.pets[idx]:
            return
        if p.pets[idx]['hp'] <= 0:
            return self.sys(p, '%s 已經倒下了,不能出戰。' % p.pets[idx]['n'])
        if p.pets[idx]['food'] <= 0:
            return self.sys(p, '%s 餓昏了,不肯出戰。' % p.pets[idx]['n'])
        self.sync_pet(b, p)
        if old:
            b.units.pop(old.id, None)
        nu = b.add(self.pet_unit(p, idx))
        nu.bar = 0
        b.pu[p.id] = nu.id
        b.fought.setdefault(p.id, set()).add(p.pets[idx]['uid'])
        p.active = idx
        p.pets_dirty = True
        self.restack(b)
        self.bfx(b, 'act', s=u.id, t=nu.id, w='owner_swap', n='換寵', ty='owner')
        self.bfx(b, 'join', id=nu.id)
        self.end_turn(u)

    def flee(self, b, p, u, now):
        chance = CLASSES[p.cls]['flee'] * (0.4 if b.boss else 1.0)
        if random.random() < chance:
            self.bfx(b, 'flee', id=u.id, ok=1)
            self.sys(p, '成功逃跑了!')
            p.ws.send({'t': 'bend', 'b': b.id, 'win': -1})
            self.leave_battle(b, p, now)
        else:
            self.bfx(b, 'flee', id=u.id, ok=0)
            self.sys(p, '逃跑失敗!')
            self.end_turn(u)

    # ----- 每個 tick -----
    def battle_tick(self, b, now, dt):
        if b.weather and now >= b.weather_until:
            b.weather = None
            self.bfx(b, 'weather', w='')
        for u in list(b.units.values()):
            if not u.alive:
                continue
            for k in [k for k, t in u.status.items() if now >= t]:
                del u.status[k]
            if 'poison' in u.status and now >= u.next_poison:
                u.next_poison = now + 2
                dmg = max(1, int(u.mhp * 0.05))
                self.bfx(b, 'hit', id=u.id, v=dmg, poison=1)
                self.damage(b, u, dmg, now)
                if b.over:
                    return
                continue
            if u.ready_at is None:
                u.bar += u.rate() * dt
                if u.bar >= 100:
                    u.bar = 100
                    u.ready_at = now
        for u in list(b.units.values()):
            if b.over:
                return
            if not self.can_act(u):
                continue
            if u.kind == 'm':
                self.ai_act(b, u, now)
            elif u.kind == 'p':
                owner = self.players.get(u.pid)
                if owner is None or owner.auto:
                    if owner is None or not self.pet_disobeys(b, u, owner, now):
                        self.ai_act(b, u, now)
                elif now - u.ready_at >= PET_TIMEOUT:
                    self.ai_act(b, u, now, smart=False)
            self.check_end(b, now)
        if not b.over:
            self.guard_check(b, now)

    def check_end(self, b, now):
        if b.over:
            return
        if not b.alive(1):
            self.end_battle(b, True, now)
        elif not any(u.kind == 'o' and u.alive for u in b.units.values()):
            self.end_battle(b, False, now)

    def end_battle(self, b, win, now):
        b.over = True
        boss_win = win and b.boss
        for pid in list(b.pids):
            p = self.players.get(pid)
            if not p:
                continue
            self.sync_pet(b, p)
            ou = b.units.get(b.ou.get(pid))
            p.hp = max(1, int(ou.hp)) if ou else 1
            p.mp = max(0, int(ou.mp)) if ou else 0
            p.battle = None
            p.steps = 0
            p.pets_dirty = p.inv_dirty = True
            self.battle_care(b, p, 'win' if win else 'lose')
            if win:
                got = []
                active = b.units.get(b.pu.get(pid))
                for pt in p.pets:
                    if pt['uid'] in b.fought.get(pid, ()) and pt['hp'] > 0:
                        share = b.exp if active is not None and active.pet is pt else b.exp // 2
                        if share:
                            self.give_pet_exp(p, pt, share)
                self.give_exp(p, b.exp)
                p.gold += b.gold
                for item in b.loot:
                    if item == 'egg_drake' or random.random() < 1.0 / len(b.pids):
                        if self.add_item(p, item):
                            got.append(ITEMS[item]['name'])
                msg = '戰鬥勝利!經驗值 +%d、金幣 +%d' % (b.exp, b.gold)
                if got:
                    msg += ',獲得 ' + '、'.join(got)
                self.sys(p, msg)
                p.ws.send({'t': 'bend', 'b': b.id, 'win': 1, 'exp': b.exp, 'gold': b.gold, 'items': got})
            else:
                for pt in p.pets:
                    if pt['hp'] <= 0:
                        pt['hp'] = 1
                p.hp = max(1, p.mhp * 3 // 10)
                p.x, p.y = SPAWN
                p.path = []
                self.add_fx('tp', p.x, p.y, id=p.id)
                self.sys(p, '戰鬥失敗……你和寵物們被送回了村莊。', 'err')
                p.ws.send({'t': 'bend', 'b': b.id, 'win': 0})
        self.bfx(b, 'bend', win=int(win))
        self.close_battle(b)
        if boss_win:
            self.boss['alive'] = False
            self.boss['respawn_at'] = now + BOSS['respawn']
            names = '、'.join(self.players[pid].name for pid in b.pids if pid in self.players)
            self.broadcast_sys('勇者 %s 擊敗了傳說中的炎龍!整個大陸都在歡呼!' % names, 'ann')

    # ---------- 每個 tick ----------
    def update_player(self, p, now, dt):
        p.moving = False
        if p.hatch:
            self.hatch_tick(p, now, dt)
        if p.battle:
            return
        bx, by = p.x, p.y
        if p.dir != (0.0, 0.0):
            self.step(p, p.x + p.dir[0] * 2, p.y + p.dir[1] * 2, p.spd, dt)
        elif p.npc is not None:
            n = self.npc_by_id[p.npc]
            if dist(p.x, p.y, n['x'], n['y']) <= 2.2:
                p.npc = None
                p.path = []
                p.face = 1 if n['x'] >= p.x else -1
                self.open_npc(p, n)
            else:
                self.chase(p, n['x'], n['y'], p.spd, dt, now)
        elif p.boss_go:
            bs = self.boss
            if not bs['alive']:
                p.boss_go = False
            elif dist(p.x, p.y, bs['x'], bs['y']) <= 3.2:
                p.boss_go = False
                p.path = []
                self.start_boss(p, now)
                return
            else:
                self.chase(p, bs['x'], bs['y'], p.spd, dt, now)
        elif p.path:
            self.follow_path(p, p.spd, dt)
        moved = dist(bx, by, p.x, p.y)
        if moved > 0:
            p.idle_since = now
            self.encounter_check(p, moved, now)

    def tick(self):
        now = time.time()
        dt = TICK
        self.tickn += 1
        for p in list(self.players.values()):
            self.update_player(p, now, dt)
        for b in list(self.battles.values()):
            self.battle_tick(b, now, dt)
        if not self.boss['alive'] and now >= self.boss['respawn_at']:
            self.boss['alive'] = True
            self.broadcast_sys('大地在震動……炎龍在北方焦土甦醒了!', 'ann')
        if now - self.last_regen >= 1.0:
            el = min(5.0, now - self.last_regen)
            self.last_regen = now
            for p in list(self.players.values()):
                self.care_tick(p, now, el)
            for p in self.players.values():
                if p.battle:
                    continue
                town = in_town(p.x, p.y)
                k = 0.08 if town else 0.02
                p.hp = min(p.mhp, p.hp + max(1, int(p.mhp * k)))
                p.mp = min(p.mmp, p.mp + max(1, int(p.mmp * k)))
                for pt in p.pets:
                    if pt['hp'] <= 0:
                        continue
                    d = derive(pt['lv'], pt['st'])
                    if pt['hp'] < d['mhp'] or pt['mp'] < d['mmp']:
                        pt['hp'] = min(d['mhp'], pt['hp'] + max(1, int(d['mhp'] * k)))
                        pt['mp'] = min(d['mmp'], pt['mp'] + max(1, int(d['mmp'] * k)))
                        if self.tickn % 100 == 0 or town:
                            p.pets_dirty = True
        if self.tickn % SNAP_EVERY == 0:
            self.send_snaps(now)
        if now - self.last_save > 30:
            self.last_save = now
            self.save()

    def battle_mood(self, b, u):
        """戰鬥中寵物頭上的泡泡"""
        pt = u.pet
        if pt is None or not u.alive:
            return ''
        if pt['food'] <= 0:
            return 'starve'
        if pt['food'] < CARE['hungry']:
            return 'hungry'
        if pt['joy'] < CARE['angry']:
            return 'angry'
        foes = b.alive(1 - u.side)
        if u.hp < u.mhp * 0.3 or (foes and max(f.lv for f in foes) >= u.lv + 5):
            return 'scared'
        return ''

    def unit_view(self, u, now, b=None):
        v = {'i': u.id, 's': u.side, 'r': u.row, 'k': u.kind, 'c': u.sp or u.cls, 'n': u.name, 'lv': u.lv,
             'el': u.el or '', 'hp': max(0, int(u.hp)), 'mh': u.mhp, 'mp': max(0, int(u.mp)), 'mm': u.mmp,
             'bar': round(u.bar, 1), 'rt': round(u.rate(), 1), 'rd': int(u.ready_at is not None),
             'st': sorted(u.status.keys()), 'pid': u.pid or 0, 'ko': int(not u.alive), 'boss': int(u.boss)}
        if u.kind == 'p' and u.pet is not None:
            v['md'] = self.battle_mood(b, u) if b else ''
            v['sy'] = int(u.sync) if u.pet['bond'] >= CARE['sync_bond'] else -1
            v['sg'] = int(u.surge)
        return v

    def send_snaps(self, now):
        fx, self.fx = self.fx, []
        ents = []
        for p in self.players.values():
            pt = p.pets[p.active] if p.pets and not p.battle and p.pets[p.active]['hp'] > 0 else None
            ents.append((p.x, p.y, {'i': p.id, 'k': 'p', 'x': round(p.x, 2), 'y': round(p.y, 2), 'n': p.name,
                                    'lv': p.lv, 'c': p.cls, 'f': p.face, 'mv': int(p.moving), 'b': p.battle or 0,
                                    'pt': pt['sp'] if pt else '', 'pn': pt['n'] if pt else '',
                                    'pm': pet_mood(pt, now - p.idle_since) if pt else ''}))
        bs = self.boss
        if bs['alive'] and not bs['battle']:
            ents.append((bs['x'], bs['y'], {'i': bs['i'], 'k': 'm', 'x': bs['x'], 'y': bs['y'], 'c': 'dragon',
                                            'f': -1, 'mv': 0, 'n': BOSS['name'], 'lv': BOSS['lv']}))
        battles = [(b.cx, b.cy, {'i': b.id, 'x': round(b.cx, 2), 'y': round(b.cy, 2), 'w': b.weather or '',
                                 'boss': int(b.boss), 'np': len(b.pids),
                                 'u': [self.unit_view(u, now, b) for u in b.units.values()]})
                   for b in self.battles.values()]
        for p in list(self.players.values()):
            e = [o for (x, y, o) in ents if abs(x - p.x) < VIEW and abs(y - p.y) < VIEW]
            bt = [o for (x, y, o) in battles if abs(x - p.x) < VIEW and abs(y - p.y) < VIEW]
            f = [o for o in fx if abs(o['x'] - p.x) < VIEW and abs(o['y'] - p.y) < VIEW]
            me = {'hp': p.hp, 'mh': p.mhp, 'mp': p.mp, 'mm': p.mmp, 'lv': p.lv, 'exp': p.exp,
                  'nx': exp_need(p.lv), 'bt': p.battle or 0, 'auto': int(p.auto), 'tg': p.btarget,
                  'hatch': int(bool(p.hatch))}
            if p.battle in self.battles:   # 戰鬥中即時更新出戰寵物的 HP/MP 到寵物資料
                self.sync_pet(self.battles[p.battle], p)
            p.ws.send({'t': 'snap', 'e': e, 'bt': bt, 'fx': f, 'me': me})
            if p.inv_dirty:
                p.inv_dirty = False
                p.ws.send({'t': 'inv', 'inv': p.inv, 'g': p.gold})
            if p.pets_dirty:
                p.pets_dirty = False
                p.ws.send(self.pets_msg(p, now))
            if p.bank_dirty:
                p.bank_dirty = False
                p.ws.send({'t': 'bank', 'bank': [pet_view(pt) for pt in p.bank], 'max': CARE['bank_max']})

    async def run(self):
        nxt = time.perf_counter()
        while True:
            try:
                self.tick()
            except Exception:
                traceback.print_exc()
            nxt += TICK
            delay = nxt - time.perf_counter()
            if delay < 0:
                nxt = time.perf_counter()
                delay = 0
            await asyncio.sleep(delay)

    async def session(self, ws):
        p = None
        try:
            while True:
                raw = await ws.recv()
                if raw is None:
                    break
                try:
                    msg = json.loads(raw)
                except ValueError:
                    continue
                if not isinstance(msg, dict):
                    continue
                if p is None:
                    if msg.get('t') == 'login':
                        p = self.login(ws, msg)
                    continue
                try:
                    self.handle(p, msg)
                except (ValueError, TypeError, KeyError):
                    pass
                except Exception:
                    traceback.print_exc()
        except (asyncio.IncompleteReadError, ConnectionError, OSError):
            pass
        finally:
            if p:
                self.logout(p)


# ============================================================
#  網路層:極簡 HTTP 靜態檔案 + WebSocket
# ============================================================
class WS:
    def __init__(self, reader, writer):
        self.r, self.w = reader, writer
        self.closed = False

    async def recv(self):
        buf = b''
        while True:
            h = await self.r.readexactly(2)
            fin, op = h[0] & 0x80, h[0] & 0x0F
            masked, ln = h[1] & 0x80, h[1] & 0x7F
            if ln == 126:
                ln = struct.unpack('>H', await self.r.readexactly(2))[0]
            elif ln == 127:
                ln = struct.unpack('>Q', await self.r.readexactly(8))[0]
            if ln > (1 << 16):
                raise ConnectionError('frame too large')
            mask = await self.r.readexactly(4) if masked else b''
            data = await self.r.readexactly(ln)
            if masked:
                k = int.from_bytes((mask * (ln // 4 + 1))[:ln], 'big')
                data = (int.from_bytes(data, 'big') ^ k).to_bytes(ln, 'big')
            if op == 8:
                return None
            if op == 9:
                self._send(10, data)
                continue
            if op == 10:
                continue
            buf += data
            if fin:
                return buf.decode('utf-8', 'replace')

    def send(self, obj):
        if self.closed:
            return
        self._send(1, json.dumps(obj, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))

    def _send(self, op, data):
        if self.closed:
            return
        n = len(data)
        if n < 126:
            hdr = struct.pack('>BB', 0x80 | op, n)
        elif n < 65536:
            hdr = struct.pack('>BBH', 0x80 | op, 126, n)
        else:
            hdr = struct.pack('>BBQ', 0x80 | op, 127, n)
        try:
            if self.w.transport.get_write_buffer_size() > 4 * 1024 * 1024:
                raise ConnectionError('client too slow')
            self.w.write(hdr + data)
        except Exception:
            self.closed = True
            try:
                self.w.close()
            except Exception:
                pass


MIME = {'.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8',
        '.css': 'text/css; charset=utf-8', '.png': 'image/png', '.ico': 'image/x-icon',
        '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml'}

# ============================================================
#  圖片管線:圖片清單 (/assets.json) 與去背工具的存檔 (/api/art,只接受本機)
# ============================================================
ASSETS = os.path.join(PUBLIC, 'assets')
ART_SRC = os.path.join(ROOT, 'art-src')     # 使用者放 AI 原圖的地方 (不進 git),檔名用中文名字,例如 噗噗.png
ART_MAX_BYTES = 4 * 1024 * 1024
PNG_SIG = b'\x89PNG\r\n\x1a\n'
SRC_EXT = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}


def src_files():
    if not os.path.isdir(ART_SRC):
        return []
    return sorted(fn for fn in os.listdir(ART_SRC)
                  if os.path.splitext(fn)[1].lower() in SRC_EXT and os.path.isfile(os.path.join(ART_SRC, fn)))


def asset_manifest():
    files = []
    for sub in ('pets', 'npcs'):
        d = os.path.join(ASSETS, sub)
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.lower().endswith('.png'):
                    files.append({'p': sub + '/' + fn, 'v': int(os.path.getmtime(os.path.join(d, fn)))})
    return {'files': files, 'art': ART, 'frames': list(ART_FRAMES), 'src': src_files(),
            'species': dict([(k, v['name']) for k, v in SPECIES.items()] + [('dragon', BOSS['name'])]),
            'npcs': {n['c']: n['n'] for n in NPCS}}


def art_path(name):
    """去背工具要存的檔名:只接受 pets/<種族>[_動作].png 或 npcs/<NPC 類別>.png,回傳完整路徑或 None"""
    if not isinstance(name, str) or not name.endswith('.png') or name.count('/') != 1:
        return None
    sub, fn = name[:-4].split('/')
    if sub == 'pets':
        base, _, frame = fn.partition('_')
        if (base not in SPECIES and base != 'dragon') or (frame and frame not in ART_FRAMES):
            return None
    elif sub == 'npcs':
        if fn not in {n['c'] for n in NPCS}:
            return None
    else:
        return None
    return os.path.join(ASSETS, sub, fn + '.png')


def save_art(name, data, delete=False):
    """存 (或刪除) 一張圖。回傳 (成功, 訊息)"""
    full = art_path(name)
    if not full:
        return False, '檔名不符合規格'
    if delete:
        if os.path.isfile(full):
            os.remove(full)
        return True, '已刪除 ' + name
    if not data.startswith(PNG_SIG) or len(data) > ART_MAX_BYTES:
        return False, '不是 PNG 圖檔,或檔案太大'
    os.makedirs(os.path.dirname(full), exist_ok=True)
    tmp = full + '.tmp'
    with open(tmp, 'wb') as f:
        f.write(data)
    os.replace(tmp, full)
    return True, '已存到 public/assets/' + name


def is_local(writer):
    peer = writer.get_extra_info('peername')
    host = peer[0] if peer else ''
    return host in ('127.0.0.1', '::1', '::ffff:127.0.0.1')


async def respond(writer, status, ctype, body):
    writer.write(('HTTP/1.1 %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nCache-Control: no-cache\r\n'
                  'Connection: close\r\n\r\n' % (status, ctype, len(body))).encode() + body)
    try:
        await writer.drain()
    except Exception:
        pass
    writer.close()


async def handle_conn(reader, writer, game):
    try:
        req = await asyncio.wait_for(reader.readuntil(b'\r\n\r\n'), 15)
    except Exception:
        writer.close()
        return
    lines = req.decode('latin-1').split('\r\n')
    try:
        method, path, _ = lines[0].split(' ', 2)
    except ValueError:
        writer.close()
        return
    headers = {}
    for line in lines[1:]:
        if ':' in line:
            k, v = line.split(':', 1)
            headers[k.strip().lower()] = v.strip()

    if headers.get('upgrade', '').lower() == 'websocket':
        key = headers.get('sec-websocket-key', '')
        acc = base64.b64encode(hashlib.sha1((key + WS_GUID).encode()).digest()).decode()
        writer.write(('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                      'Sec-WebSocket-Accept: %s\r\n\r\n' % acc).encode())
        await writer.drain()
        ws = WS(reader, writer)
        await game.session(ws)
        ws.closed = True
        try:
            writer.close()
        except Exception:
            pass
        return

    path, _, query = path.partition('?')
    path = unquote(path)
    if path == '/assets.json':
        body = json.dumps(asset_manifest(), ensure_ascii=False).encode('utf-8')
        return await respond(writer, '200 OK', MIME['.json'], body)
    if path == '/api/src':   # 去背工具讀 art-src/ 裡的原圖 (只接受本機、只能讀清單裡的檔案)
        name = parse_qs(query).get('f', [''])[0]
        if not is_local(writer) or name not in src_files():
            return await respond(writer, '404 Not Found', 'text/plain', b'404 Not Found')
        with open(os.path.join(ART_SRC, name), 'rb') as f:
            body = f.read()
        return await respond(writer, '200 OK', SRC_EXT[os.path.splitext(name)[1].lower()], body)
    if path == '/api/art':
        if method != 'POST':
            return await respond(writer, '405 Method Not Allowed', 'text/plain', b'POST only')
        if not is_local(writer):
            return await respond(writer, '403 Forbidden', MIME['.json'],
                                 json.dumps({'ok': False, 'msg': '只接受本機 (localhost) 的連線'}, ensure_ascii=False).encode('utf-8'))
        q = parse_qs(query)
        n = int(headers.get('content-length', '0') or 0)
        if n > ART_MAX_BYTES:
            ok, msg = False, '檔案太大'
        else:
            data = await reader.readexactly(n) if n > 0 else b''
            ok, msg = save_art(q.get('f', [''])[0], data, delete=q.get('del', [''])[0] == '1')
        return await respond(writer, '200 OK', MIME['.json'], json.dumps({'ok': ok, 'msg': msg}, ensure_ascii=False).encode('utf-8'))
    if path == '/':
        path = '/index.html'
    full = os.path.normpath(os.path.join(PUBLIC, path.lstrip('/')))
    if not full.startswith(PUBLIC) or not os.path.isfile(full):
        body, status, ctype = b'404 Not Found', '404 Not Found', 'text/plain'
    else:
        with open(full, 'rb') as f:
            body = f.read()
        status, ctype = '200 OK', MIME.get(os.path.splitext(full)[1].lower(), 'application/octet-stream')
    await respond(writer, status, ctype, body)


async def main():
    game = Game()
    server = await asyncio.start_server(lambda r, w: handle_conn(r, w, game), '0.0.0.0', PORT)
    try:
        lan = socket.gethostbyname(socket.gethostname())
    except Exception:
        lan = '你的區網IP'
    print('=' * 52)
    print('  幻想之境 Online 伺服器已啟動!')
    print('  本機遊玩:  http://localhost:%d' % PORT)
    print('  區網朋友:  http://%s:%d' % (lan, PORT))
    print('  寵物種類:  %d    已註冊角色: %d' % (len(SPECIES), len(game.accounts)))
    print('  按 Ctrl+C 關閉伺服器 (會自動存檔)')
    print('=' * 52)
    try:
        await game.run()
    finally:
        game.save()
        server.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('伺服器已關閉,資料已存檔。')
