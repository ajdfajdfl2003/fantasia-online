# -*- coding: utf-8 -*-
"""
幻想之境 Online — 遊戲數值資料

想調整平衡,改這個檔案就好,改完重開伺服器。
寵物素質、技能樹、孵蛋溫濕度參考自《寵物王 Online》(2003) 的攻略資料,見 docs/寵物王研究筆記.md
"""

# ============================================================
#  屬性相剋
# ============================================================
ELEMENTS = {'earth': '地', 'water': '水', 'wind': '風', 'fire': '火', 'light': '光', 'dark': '暗'}
ELEMENT_COLORS = {'earth': '#b08040', 'water': '#3a80e0', 'wind': '#50c080',
                  'fire': '#e85020', 'light': '#f0d040', 'dark': '#7040a0'}
# (攻擊方, 防守方):水剋火、火剋風、風剋地、地剋水,光暗互剋
STRONG = {('water', 'fire'), ('fire', 'wind'), ('wind', 'earth'), ('earth', 'water'),
          ('light', 'dark'), ('dark', 'light')}


def elem_mult(atk_el, def_el):
    if not atk_el or not def_el:
        return 1.0
    if (atk_el, def_el) in STRONG:
        return 1.3
    if (def_el, atk_el) in STRONG:
        return 0.75
    return 1.0


# 天氣 (法師可以改變):屬性 → 倍率
WEATHER = {
    'sun':  {'name': '烈日', 'fire': 1.3, 'light': 1.3, 'water': 0.8},
    'rain': {'name': '暴雨', 'water': 1.3, 'wind': 1.3, 'fire': 0.7},
}

FAMILIES = {'beast': '野獸屬', 'bug': '蟲獸屬', 'wing': '翼獸屬', 'humanoid': '類人屬', 'fairy': '妖精屬'}

# ============================================================
#  寵物技能
#  type: phys 物理 / mag 魔法 / status 狀態 / heal 治療
#  target: enemy 單一敵人 / enemies 全體敵人 / ally 單一隊友
# ============================================================
PET_SKILLS = {
    'tackle':     {'name': '撞擊', 'mp': 3, 'type': 'phys', 'mult': 1.4, 'target': 'enemy', 'fx': 'slam'},
    'double':     {'name': '二段攻擊', 'mp': 5, 'type': 'phys', 'mult': 0.8, 'hits': 2, 'target': 'enemy', 'fx': 'slash'},
    'triple':     {'name': '三段攻擊', 'mp': 9, 'type': 'phys', 'mult': 0.75, 'hits': 3, 'target': 'enemy', 'fx': 'slash'},
    'sneak':      {'name': '偷襲', 'mp': 6, 'type': 'phys', 'mult': 1.3, 'pierce': True, 'target': 'enemy', 'fx': 'slash',
                   'desc': '無視對方防禦'},
    'poison':     {'name': '毒擊', 'mp': 6, 'type': 'phys', 'mult': 0.9, 'status': ('poison', 10), 'target': 'enemy', 'fx': 'poison'},
    'drain':      {'name': '吸血', 'mp': 6, 'type': 'phys', 'mult': 1.1, 'el': 'dark', 'drain': 0.5, 'target': 'enemy', 'fx': 'drain',
                   'desc': '吸收造成傷害的一半'},
    'rock':       {'name': '落石', 'mp': 6, 'type': 'mag', 'el': 'earth', 'mult': 1.6, 'target': 'enemy', 'fx': 'rock'},
    'quake':      {'name': '地震', 'mp': 14, 'type': 'mag', 'el': 'earth', 'mult': 1.1, 'target': 'enemies', 'fx': 'quake'},
    'fireball':   {'name': '火球', 'mp': 6, 'type': 'mag', 'el': 'fire', 'mult': 1.6, 'target': 'enemy', 'fx': 'fire'},
    'flamerain':  {'name': '焰星雨', 'mp': 14, 'type': 'mag', 'el': 'fire', 'mult': 1.1, 'target': 'enemies', 'fx': 'flamerain'},
    'iceball':    {'name': '冰球', 'mp': 6, 'type': 'mag', 'el': 'water', 'mult': 1.6, 'target': 'enemy', 'fx': 'ice'},
    'icicle':     {'name': '冰柱', 'mp': 14, 'type': 'mag', 'el': 'water', 'mult': 1.1, 'target': 'enemies', 'fx': 'icicle'},
    'gale':       {'name': '狂風', 'mp': 6, 'type': 'mag', 'el': 'wind', 'mult': 1.6, 'target': 'enemy', 'fx': 'wind'},
    'storm':      {'name': '風暴', 'mp': 14, 'type': 'mag', 'el': 'wind', 'mult': 1.1, 'target': 'enemies', 'fx': 'storm'},
    'laser':      {'name': '雷射', 'mp': 7, 'type': 'mag', 'el': 'light', 'mult': 1.7, 'target': 'enemy', 'fx': 'laser'},
    'holy':       {'name': '聖光陣', 'mp': 14, 'type': 'mag', 'el': 'light', 'mult': 1.1, 'target': 'enemies', 'fx': 'holy'},
    'darkcircle': {'name': '暗法陣', 'mp': 14, 'type': 'mag', 'el': 'dark', 'mult': 1.1, 'target': 'enemies', 'fx': 'darkc'},
    'sleep':      {'name': '睡眠', 'mp': 8, 'type': 'status', 'status': ('sleep', 6), 'chance': 0.6, 'target': 'enemy', 'fx': 'sleep',
                   'desc': '60% 機率讓敵人睡著 6 秒 (被打會醒)'},
    'weaken':     {'name': '防禦弱化', 'mp': 6, 'type': 'status', 'status': ('defdown', 15), 'chance': 1.0, 'target': 'enemy',
                   'fx': 'debuff', 'desc': '敵人防禦力下降 30%,持續 15 秒'},
    'heal':       {'name': '治療', 'mp': 8, 'type': 'heal', 'mult': 0.3, 'target': 'ally', 'fx': 'heal',
                   'desc': '恢復隊友 30% HP'},
    'breath':     {'name': '龍息', 'mp': 16, 'type': 'mag', 'el': 'fire', 'mult': 1.4, 'target': 'enemies', 'fx': 'breath'},
}

# ============================================================
#  寵物種族
#  base: 初始 (力量, 體質, 智力, 敏捷)    grow: 每升一級得到的自由點數
#  pref: 自動配點 / 天生素質的偏好權重      skills: (技能, 學會等級)
#  cap: 捕捉難易度 (越高越好抓,0 = 無法捕捉)
#  egg: 有蛋的寵物 (商店價格、最佳孵化溫度與濕度)
# ============================================================
SPECIES = {
    'poring':   {'name': '噗噗', 'el': 'earth', 'fam': 'bug', 'base': (15, 14, 9, 12), 'grow': 4, 'pref': (1, 2, 1, 1),
                 'skills': [('tackle', 1), ('heal', 5), ('quake', 10)], 'cap': 0.75},
    'slime':    {'name': '綠史萊姆', 'el': 'water', 'fam': 'bug', 'base': (16, 10, 10, 12), 'grow': 5, 'pref': (2, 1, 1, 1),
                 'skills': [('double', 1), ('iceball', 5), ('sneak', 10)], 'cap': 0.7},
    'goblin':   {'name': '哥布林', 'el': 'earth', 'fam': 'humanoid', 'base': (14, 14, 8, 12), 'grow': 4, 'pref': (2, 2, 0, 1),
                 'skills': [('tackle', 1), ('sneak', 5), ('heal', 10)], 'cap': 0.6},
    'wolf':     {'name': '野狼', 'el': 'wind', 'fam': 'beast', 'base': (18, 13, 8, 17), 'grow': 4, 'pref': (2, 1, 0, 2),
                 'skills': [('double', 1), ('gale', 5), ('triple', 10)], 'cap': 0.55},
    'skeleton': {'name': '骷髏兵', 'el': 'dark', 'fam': 'humanoid', 'base': (20, 10, 16, 15), 'grow': 5, 'pref': (2, 1, 1, 1),
                 'skills': [('double', 1), ('darkcircle', 5), ('drain', 10)], 'cap': 0.45},
    'imp':      {'name': '小火妖', 'el': 'fire', 'fam': 'fairy', 'base': (12, 12, 22, 16), 'grow': 6, 'pref': (0, 1, 3, 1),
                 'skills': [('fireball', 1), ('weaken', 5), ('flamerain', 10)], 'cap': 0.4,
                 'egg': {'price': 450, 'temp': 90, 'hum': 10}},
    'dove':     {'name': '彩虹鴿', 'el': 'light', 'fam': 'wing', 'base': (22, 18, 15, 18), 'grow': 4, 'pref': (2, 1, 1, 1),
                 'skills': [('double', 1), ('laser', 5), ('triple', 10)], 'cap': 0.5,
                 'egg': {'price': 260, 'temp': 60, 'hum': 35}},
    'fox':      {'name': '月狐', 'el': 'water', 'fam': 'beast', 'base': (16, 10, 19, 16), 'grow': 4, 'pref': (0, 1, 2, 1),
                 'skills': [('iceball', 1), ('sleep', 5), ('icicle', 10)], 'cap': 0.45,
                 'egg': {'price': 260, 'temp': 50, 'hum': 60}},
    'bat':      {'name': '吸血蝙蝠', 'el': 'dark', 'fam': 'wing', 'base': (19, 18, 18, 18), 'grow': 5, 'pref': (1, 1, 1, 1),
                 'skills': [('drain', 1), ('sleep', 5), ('darkcircle', 10)], 'cap': 0.45,
                 'egg': {'price': 320, 'temp': 60, 'hum': 60}},
    'griffin':  {'name': '獅鷲獸', 'el': 'light', 'fam': 'wing', 'base': (20, 20, 13, 20), 'grow': 5, 'pref': (2, 1, 1, 2),
                 'skills': [('tackle', 1), ('holy', 5), ('weaken', 10)], 'cap': 0.3,
                 'egg': {'price': 900, 'temp': 60, 'hum': 60}},
    'drake':    {'name': '幼龍', 'el': 'fire', 'fam': 'wing', 'base': (22, 20, 20, 18), 'grow': 6, 'pref': (1, 1, 1, 1),
                 'skills': [('tackle', 1), ('fireball', 3), ('breath', 8)], 'cap': 0,
                 'egg': {'price': 3000, 'temp': 95, 'hum': 20, 'shop': False}},
}


def pet_skills(sp, lv):
    return [s for s, need in SPECIES[sp]['skills'] if lv >= need]


def derive(lv, st):
    """由 (力, 體, 智, 敏) 算出戰鬥數值 — 公式參考寵物王:1 體質 = 4 HP、1 智力 = 3 MP"""
    s, v, i, a = st
    return {'mhp': 30 + v * 4 + lv * 5, 'mmp': 10 + i * 3,
            'atk': int(s * 1.5 + lv), 'matk': int(i * 1.4 + lv),
            'def': int(v * 0.5 + lv * 0.5), 'mdef': int(i * 0.4 + v * 0.2 + lv * 0.5),
            'spd': 18 + a * 0.8, 'eva': min(0.25, 0.03 + a * 0.0015)}


def exp_need(lv):
    return int(10 + 12 * lv ** 1.7)


def stars(q):
    """天生素質點 (0~12) → 星等"""
    return 5 if q >= 12 else 4 if q >= 9 else 3 if q >= 6 else 2 if q >= 3 else 1


# 野生寵物的天生素質分布 (0~12 點的權重):大多普通,12 點極品非常稀有
WILD_QUALITY_WEIGHTS = [8, 10, 12, 12, 11, 10, 8, 6, 4, 3, 2, 1, 0.4]
WILD_POWER = 0.72          # 野生怪的 HP 與攻擊力倍率 (比玩家養的寵物弱一點)

# ============================================================
#  主人職業 (原作 5 職業) — 主人不能攻擊,只能輔助
#  eff 種類:buff / debuff / heal / shield / revive / bar / weather / mpall / sleep / hasteall
# ============================================================
CLASSES = {
    'knight': {'name': '騎士', 'hp': 120, 'mp': 30, 'ghp': 15, 'gmp': 4, 'spd': 20,
               'enc': 1.0, 'cap': 1.0, 'flee': 0.7, 'desc': '強化寵物攻防,削弱敵人',
               'skills': [
                   {'name': '鼓舞', 'mp': 8, 'lv': 1, 'target': 'ally', 'eff': 'buff', 'st': 'atkup', 'dur': 15,
                    'desc': '我方寵物攻擊力提升 30%,持續 15 秒'},
                   {'name': '守護', 'mp': 8, 'lv': 3, 'target': 'ally', 'eff': 'buff', 'st': 'defup', 'dur': 15,
                    'desc': '我方寵物防禦力提升 40%,持續 15 秒'},
                   {'name': '威嚇', 'mp': 15, 'lv': 6, 'target': 'enemies', 'eff': 'debuff', 'st': 'atkdown', 'dur': 12,
                    'desc': '全體敵人攻擊力下降 20%,持續 12 秒'}]},
    'hunter': {'name': '獵人', 'hp': 100, 'mp': 35, 'ghp': 12, 'gmp': 5, 'spd': 20,
               'enc': 0.7, 'cap': 1.35, 'flee': 0.9, 'desc': '操控時間棒,捕捉成功率高,遇敵率低',
               'skills': [
                   {'name': '疾風', 'mp': 6, 'lv': 1, 'target': 'ally', 'eff': 'bar', 'val': 50,
                    'desc': '我方寵物的時間棒立刻增加 50%'},
                   {'name': '遲緩', 'mp': 8, 'lv': 3, 'target': 'enemy', 'eff': 'debuff', 'st': 'slow', 'dur': 10, 'val': -50,
                    'desc': '敵人時間棒減少 50%,並變慢 10 秒'},
                   {'name': '看破', 'mp': 10, 'lv': 6, 'target': 'enemy', 'eff': 'debuff', 'st': 'defdown', 'dur': 15,
                    'desc': '敵人防禦力下降 30%,持續 15 秒'}]},
    'priest': {'name': '牧師', 'hp': 95, 'mp': 50, 'ghp': 11, 'gmp': 7, 'spd': 20,
               'enc': 1.1, 'cap': 1.0, 'flee': 0.7, 'desc': '治療寵物、防護罩、復活',
               'skills': [
                   {'name': '治癒術', 'mp': 8, 'lv': 1, 'target': 'ally', 'eff': 'heal', 'val': 0.35,
                    'desc': '恢復我方寵物 35% HP'},
                   {'name': '防護罩', 'mp': 10, 'lv': 3, 'target': 'ally', 'eff': 'shield', 'val': 0.3,
                    'desc': '替寵物張開可吸收 30% 最大 HP 傷害的護罩'},
                   {'name': '復活術', 'mp': 20, 'lv': 6, 'target': 'ally', 'eff': 'revive', 'val': 0.4,
                    'desc': '讓倒下的寵物以 40% HP 復活'}]},
    'mage':   {'name': '法師', 'hp': 95, 'mp': 50, 'ghp': 11, 'gmp': 7, 'spd': 20,
               'enc': 1.3, 'cap': 1.0, 'flee': 0.7, 'desc': '強化寵物魔法,改變戰場天氣',
               'skills': [
                   {'name': '魔力增幅', 'mp': 8, 'lv': 1, 'target': 'ally', 'eff': 'buff', 'st': 'matkup', 'dur': 15,
                    'desc': '我方寵物魔法攻擊力提升 35%,持續 15 秒'},
                   {'name': '烈日', 'mp': 12, 'lv': 3, 'target': 'none', 'eff': 'weather', 'val': 'sun', 'dur': 25,
                    'desc': '天氣變成烈日 25 秒:火、光屬性 +30%,水屬性 -20%'},
                   {'name': '暴雨', 'mp': 12, 'lv': 6, 'target': 'none', 'eff': 'weather', 'val': 'rain', 'dur': 25,
                    'desc': '天氣變成暴雨 25 秒:水、風屬性 +30%,火屬性 -30%'}]},
    'bard':   {'name': '吟遊詩人', 'hp': 100, 'mp': 45, 'ghp': 12, 'gmp': 6, 'spd': 25,
               'enc': 1.0, 'cap': 1.0, 'flee': 0.75, 'desc': '時間棒最快,用歌聲支援全隊',
               'skills': [
                   {'name': '魔力之歌', 'mp': 6, 'lv': 1, 'target': 'none', 'eff': 'mpall', 'val': 15,
                    'desc': '我方全體寵物恢復 MP'},
                   {'name': '安眠曲', 'mp': 10, 'lv': 3, 'target': 'enemy', 'eff': 'sleep', 'val': 0.65, 'dur': 6,
                    'desc': '65% 機率讓敵人睡著 6 秒 (被打會醒)'},
                   {'name': '戰歌', 'mp': 15, 'lv': 6, 'target': 'none', 'eff': 'hasteall', 'st': 'haste', 'dur': 15,
                    'desc': '我方全體寵物時間棒加快 35%,持續 15 秒'}]},
}

STATUS_NAMES = {'atkup': '攻↑', 'defup': '防↑', 'matkup': '魔↑', 'atkdown': '攻↓', 'defdown': '防↓',
                'slow': '緩', 'haste': '速', 'sleep': '睡', 'poison': '毒', 'guard': '防禦', 'shield': '盾'}

# ============================================================
#  道具
# ============================================================
ITEMS = {
    'red_potion':  {'name': '紅色藥水', 'type': 'use', 'hp': 80, 'price': 15, 'icon': 'potion', 'col': '#e03030',
                    'desc': '恢復寵物 HP 80'},
    'blue_potion': {'name': '藍色藥水', 'type': 'use', 'mp': 40, 'price': 25, 'icon': 'potion', 'col': '#3060e0',
                    'desc': '恢復寵物 MP 40'},
    'revive_herb': {'name': '復活草', 'type': 'use', 'revive': 0.3, 'price': 60, 'icon': 'herb', 'col': '#40c040',
                    'desc': '讓倒下的寵物以 30% HP 復活'},
    'seal_card':   {'name': '封印卡', 'type': 'seal', 'price': 30, 'icon': 'card', 'col': '#b890ff',
                    'desc': '戰鬥中對敵人使用,把牠封印成自己的寵物。對手血越少越容易成功'},
}
for _k, _sp in SPECIES.items():
    if 'egg' in _sp:
        ITEMS['egg_' + _k] = {'name': _sp['name'] + '蛋', 'type': 'egg', 'sp': _k, 'price': _sp['egg']['price'],
                              'icon': 'egg', 'col': ELEMENT_COLORS[_sp['el']],
                              'desc': '%s屬性的蛋。拿到孵化屋孵化吧!' % ELEMENTS[_sp['el']]}

SHOP_ITEMS = ['red_potion', 'blue_potion', 'revive_herb', 'seal_card']
EGG_SHOP = ['egg_' + k for k, sp in SPECIES.items() if 'egg' in sp and sp['egg'].get('shop', True)]

# ============================================================
#  孵蛋
# ============================================================
HATCH_TIME = 60          # 秒
HATCH_WARMUP = 20        # 前 20 秒是「預熱」,用來摸索,不計分
HATCH_HINTS = {
    'fire': '火屬性的蛋啊,最喜歡又熱又乾燥的地方。',
    'water': '水屬性的蛋喜歡溫和又潮濕……像雨後的森林那樣。',
    'light': '光屬性的蛋喜歡暖洋洋的,不過別太潮濕。',
    'dark': '暗屬性的蛋?牠們喜歡溫暖又悶濕的感覺。',
}

# ============================================================
#  遇敵區域 (依距離村莊中心的遠近)
#  mobs: (種族, 最低等級, 最高等級, 權重)    rare: (種族, 機率, 最低等級, 最高等級)
# ============================================================
ZONES = [
    {'name': '艾爾文草原', 'd': (0, 22), 'max': 2,
     'mobs': [('poring', 1, 2, 5), ('slime', 1, 3, 3)], 'rare': ('fox', 0.03, 3, 4)},
    {'name': '迷霧森林', 'd': (22, 32), 'max': 3,
     'mobs': [('slime', 4, 7, 2), ('goblin', 5, 8, 4), ('wolf', 6, 8, 2)], 'rare': ('dove', 0.03, 7, 8)},
    {'name': '狼嚎之丘', 'd': (32, 40), 'max': 3,
     'mobs': [('wolf', 8, 12, 4), ('goblin', 8, 10, 2), ('skeleton', 10, 13, 3)], 'rare': ('bat', 0.03, 11, 12)},
    {'name': '亡者荒原', 'd': (40, 99), 'max': 4,
     'mobs': [('skeleton', 13, 17, 4), ('wolf', 12, 15, 2), ('bat', 13, 16, 2)], 'rare': ('griffin', 0.02, 15, 16)},
]
ENCOUNTER_RATE = 0.045   # 每走一格的遇敵機率
ENCOUNTER_MIN_STEPS = 6  # 戰鬥結束後至少走幾格才會再遇敵
ROAD_ENCOUNTER = 0.35    # 走在道路上的遇敵倍率

# ============================================================
#  BOSS:炎龍
# ============================================================
BOSS = {'name': '炎龍', 'lv': 25, 'el': 'fire', 'hp': 3000, 'hp_per_player': 1200, 'mp': 999,
        'atk': 75, 'matk': 65, 'def': 20, 'mdef': 16, 'spd': 26, 'eva': 0.02,
        'exp': 1500, 'gold': 300, 'respawn': 180}
