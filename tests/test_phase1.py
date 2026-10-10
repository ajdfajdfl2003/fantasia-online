# -*- coding: utf-8 -*-
"""
階段 1 無頭測試:直接呼叫伺服器邏輯,用假時鐘快轉,不需要開瀏覽器。

用法:python tests/test_phase1.py          (只跑功能測試)
     python tests/test_phase1.py --balance (再加上戰鬥平衡模擬)
"""
import json
import math
import os
import random
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import game_data as gd   # noqa: E402
import server            # noqa: E402

# ---------- 測試環境 ----------
clock = [1000000.0]
server.time.time = lambda: clock[0]        # 假時鐘
TMP = tempfile.mkdtemp()
server.DATA_DIR = TMP
server.SAVE_FILE = os.path.join(TMP, 'players.json')


class FakeWS:
    def __init__(self):
        self.msgs, self.chats, self.closed = [], [], False

    def send(self, o):
        o = json.loads(json.dumps(o))
        if o['t'] == 'chat':
            self.chats.append(o['m'])
        self.msgs.append(o)
        if len(self.msgs) > 300:
            del self.msgs[:100]

    def last(self, t):
        return next((m for m in reversed(self.msgs) if m['t'] == t), None)


results = []


def check(name, cond, info=''):
    results.append((name, bool(cond)))
    print(('  PASS ' if cond else '  FAIL ') + name + (('  — ' + str(info)) if info and not cond else ''))


def run(g, sec):
    for _ in range(int(round(sec / server.TICK))):
        clock[0] += server.TICK
        g.tick()


def run_until(g, cond, limit=120):
    for _ in range(int(limit / server.TICK)):
        if cond():
            return True
        clock[0] += server.TICK
        g.tick()
    return cond()


def find_spot(g, dmin, dmax, road=False):
    rnd = random.Random(dmin * 7 + dmax)
    cand = []
    for i in range(server.W * server.H):
        x, y = i % server.W + 0.5, i // server.W + 0.5
        d = server.dist(x, y, *server.CENTER)
        t = g.tiles[i]
        if dmin <= d < dmax and g.can_stand(x, y) and not server.in_town(x, y, 1) and t != server.T_ASH:
            if road == (t in (server.T_SAND, server.T_BRIDGE)):
                cand.append((x, y))
    return rnd.choice(cand)


def login(g, name, cls):
    p = g.login(FakeWS(), {'name': name, 'pass': 'x', 'cls': cls})
    assert p, name
    return p


def battle_of(g, p):
    return g.battles.get(p.battle)


def make_ready(u):
    u.bar = 100
    u.ready_at = clock[0]


def controlled_battle(g, p, sp='slime', lv=3, n=1, tough=True):
    """在玩家腳下開一場可控制的戰鬥:敵人不會行動、血很多"""
    b = g.new_battle(p.x, p.y)
    g.add_player(b, p, clock[0])
    for _ in range(n):
        u = g.wild_unit(sp, lv)
        if tough:
            u.mhp = u.hp = 99999
            u.spd = 0
        b.add(u)
    g.restack(b)
    return b


# ============================================================
def test_basics(g):
    print('\n[登入與新角色]')
    for cls in gd.CLASSES:
        p = login(g, 'T_' + cls, cls)
        check('%s 建立角色,送一隻噗噗' % cls, len(p.pets) == 1 and p.pets[0]['sp'] == 'poring')
        check('%s 新手道具 (封印卡 5)' % cls, g.count_item(p, 'seal_card') == 5)
    m = g.players[max(g.players)].ws.last('welcome')
    check('welcome 帶有寵物/職業/技能資料', m and 'species' in m and 'classes' in m and 'pskills' in m)


def test_encounter(g):
    print('\n[隨機遇敵]')
    p = g.by_name['T_knight']
    p.x, p.y = find_spot(g, 12, 18)
    p.steps = server.ENCOUNTER_MIN_STEPS
    p.dir = (1.0, 0.0)
    ok = run_until(g, lambda: p.battle is not None or p.dir == (0.0, 0.0), 60)
    if p.battle is None:   # 撞牆就換方向繼續走
        for d in ((-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)) * 3:
            p.dir = d
            if run_until(g, lambda: p.battle is not None, 8):
                break
    b = battle_of(g, p)
    check('野外走路會遇敵', b is not None)
    if not b:
        return
    enemies = b.alive(1)
    check('遇到 1~2 隻草原寵物', 1 <= len(enemies) <= 2 and all(e.sp in ('poring', 'slime', 'fox') for e in enemies),
          [e.sp for e in enemies])
    check('戰鬥中移動指令無效', (g.handle(p, {'t': 'move', 'x': p.x + 5, 'y': p.y}) or True) and p.path == [])
    pu = b.units[b.pu[p.id]]
    ok = run_until(g, lambda: pu.ready_at is not None, 10)
    check('寵物時間棒會集滿', ok)
    tg = enemies[0]
    hp0 = tg.hp
    g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'atk', 'tg': tg.id})
    check('下指令攻擊會造成傷害或 MISS', tg.hp < hp0 or any(f['k'] == 'hit' and f.get('v') == 0 for f in g.fx) or not tg.alive)
    check('行動後時間棒歸零', pu.bar == 0 and pu.ready_at is None)
    p.auto = True
    run_until(g, lambda: p.battle is None, 120)
    check('自動戰鬥會打完', p.battle is None)
    end = p.ws.last('bend')
    check('收到結算訊息', end is not None)
    p.auto = False
    # 村莊內不遇敵
    p.x, p.y = 47.5, 50.5
    p.steps = 99
    g.encounter_check(p, 50, clock[0])
    check('村莊內不會遇敵', p.battle is None)
    # 寵物全倒不遇敵
    p.x, p.y = find_spot(g, 12, 18)
    hp = [pt['hp'] for pt in p.pets]
    for pt in p.pets:
        pt['hp'] = 0
    g.encounter_check(p, 50, clock[0])
    check('寵物全倒時不會遇敵', p.battle is None)
    for pt, h in zip(p.pets, hp):
        pt['hp'] = max(1, h)


def test_capture_swap(g):
    print('\n[捕捉 / 換寵 / 道具]')
    p = g.by_name['T_hunter']
    p.x, p.y = find_spot(g, 12, 18)
    b = controlled_battle(g, p, 'slime', 3, tough=False)
    tg = b.alive(1)[0]
    tg.spd = 0
    tg.hp = 1
    ou = b.units[b.ou[p.id]]
    cards0 = g.count_item(p, 'seal_card')
    random.seed(1)
    caught = False
    for _ in range(5):
        make_ready(ou)
        g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'cap', 'tg': tg.id})
        if len(p.pets) == 2:
            caught = True
            break
    check('捕捉成功', caught, g.count_item(p, 'seal_card'))
    check('封印卡有消耗', g.count_item(p, 'seal_card') < cards0)
    if caught:
        pt = p.pets[1]
        check('捕捉的寵物保留等級', pt['lv'] == 3 and pt['sp'] == 'slime')
        check('等級點數是未分配狀態', pt['pts'] == gd.SPECIES['slime']['grow'] * 2, pt['pts'])
        check('天生素質在 0~12', 0 <= pt['q'] <= 12)
    check('敵人被抓光 → 戰鬥勝利', p.battle is None)
    # 換寵、道具、復活
    b = controlled_battle(g, p, 'poring', 2)
    ou, pu = b.units[b.ou[p.id]], b.units[b.pu[p.id]]
    make_ready(ou)
    g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'swap', 'i': 1})
    nu = b.units.get(b.pu[p.id])
    check('換寵', nu is not None and nu.sp == 'slime' and p.active == 1 and pu.id not in b.units)
    nu.hp = 10
    make_ready(ou)
    g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'item', 'item': 'red_potion'})
    check('戰鬥中紅色藥水補寵物', nu.hp > 10, nu.hp)
    g.ko(b, nu, clock[0])
    check('寵物倒下', not nu.alive and p.pets[1]['hp'] == 0)
    g.add_item(p, 'revive_herb')
    make_ready(ou)
    g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'item', 'item': 'revive_herb'})
    check('復活草救回寵物', nu.alive and nu.hp > 0)
    check('戰鬥中還沒結束', p.battle == b.id)
    # 逃跑
    random.seed(3)
    for _ in range(10):
        make_ready(ou)
        g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'flee'})
        if p.battle is None:
            break
    check('獵人逃跑成功', p.battle is None and b.id not in g.battles)
    check('逃跑後寵物 HP 寫回資料', p.pets[1]['hp'] == nu.hp)


def test_class_skills(g):
    print('\n[五職業輔助技能]')
    for cls in gd.CLASSES:
        p = g.by_name['T_' + cls]
        p.lv = 6
        p.recalc()
        p.hp, p.mp = p.mhp, p.mmp
        if p.battle:
            g.leave_battle(g.battles[p.battle], p, clock[0])
        p.x, p.y = find_spot(g, 12, 18)
        for pt in p.pets:
            d = gd.derive(pt['lv'], pt['st'])
            pt['hp'], pt['mp'] = d['mhp'], d['mmp']
        b = controlled_battle(g, p, 'goblin', 5, n=2)
        ou, pu = b.units[b.ou[p.id]], b.units[b.pu[p.id]]
        e1 = b.alive(1)[0]
        pu.spd = 0
        for i, sk in enumerate(gd.CLASSES[cls]['skills']):
            ou.mp = ou.mmp
            if sk['eff'] == 'revive':
                g.ko(b, pu, clock[0])
            if sk['eff'] == 'heal':
                pu.hp = 1
            make_ready(ou)
            before = (pu.hp, pu.shield, pu.bar, dict(pu.status), dict(e1.status), e1.bar, b.weather, pu.mp, pu.alive)
            g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'oskill', 's': i, 'tg': e1.id if sk['target'] == 'enemy' else pu.id})
            eff = sk['eff']
            if eff == 'buff':
                ok = sk['st'] in pu.status
            elif eff == 'debuff':
                ok = sk['st'] in e1.status
            elif eff == 'bar':
                ok = pu.bar > before[2]
            elif eff == 'heal':
                ok = pu.hp > before[0]
            elif eff == 'shield':
                ok = pu.shield > 0
            elif eff == 'revive':
                ok = pu.alive and not before[8]
            elif eff == 'weather':
                ok = b.weather == sk['val']
            elif eff == 'mpall':
                ok = True   # 寵物 MP 本來就滿,只檢查沒有出錯
            elif eff == 'sleep':
                ok = any(f['k'] == 'st' and f['st'] == 'sleep' for f in g.fx)
            elif eff == 'hasteall':
                ok = 'haste' in pu.status
            else:
                ok = False
            check('%s「%s」' % (gd.CLASSES[cls]['name'], sk['name']), ok and ou.ready_at is None and ou.mp == ou.mmp - sk['mp'])
        g.leave_battle(b, p, clock[0])


def test_pet_skills_ai(g):
    print('\n[寵物技能與傷害]')
    p = g.by_name['T_mage']
    p.x, p.y = find_spot(g, 12, 18)
    p.pets.append(server.new_pet('imp', 10, 6))
    p.active = len(p.pets) - 1
    b = controlled_battle(g, p, 'wolf', 8, n=3)
    pu = b.units[b.pu[p.id]]
    check('Lv.10 小火妖學會 3 個技能', pu.skills == ['fireball', 'weaken', 'flamerain'], pu.skills)
    enemies = b.alive(1)
    hp0 = [e.hp for e in enemies]
    make_ready(pu)
    g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'skill', 's': 'flamerain'})
    check('焰星雨打到全體敵人', all(e.hp < h for e, h in zip(enemies, hp0)))
    # 屬性相剋:火打風 ×1.3
    random.seed(5)
    e = enemies[0]
    e.status = {}
    d_strong = []
    for _ in range(30):
        h = e.hp
        g.hit(b, pu, e, 'mag', 1.6, clock[0], 'fire')
        d_strong.append(h - e.hp)
    slime = g.wild_unit('slime', 8)
    slime.mhp = slime.hp = 99999
    slime.mdf = e.mdf
    b.add(slime)
    d_weak = []
    for _ in range(30):
        h = slime.hp
        g.hit(b, pu, slime, 'mag', 1.6, clock[0], 'fire')
        d_weak.append(h - slime.hp)
    check('火剋風 > 火被水剋', sum(d_strong) > sum(d_weak) * 1.5, (sum(d_strong), sum(d_weak)))
    b.weather = 'sun'
    d_sun = []
    for _ in range(30):
        h = e.hp
        g.hit(b, pu, e, 'mag', 1.6, clock[0], 'fire')
        d_sun.append(h - e.hp)
    check('烈日加強火屬性', sum(d_sun) > sum(d_strong) * 1.15, (sum(d_sun), sum(d_strong)))
    # 連動傷害
    ou = b.units[b.ou[p.id]]
    oh = ou.hp
    g.damage(b, pu, 100, clock[0])
    check('寵物受傷,主人連動扣血 15%', oh - ou.hp == 15, oh - ou.hp)
    # 睡眠被打會醒
    e.status['sleep'] = clock[0] + 10
    check('睡眠中時間棒停止', e.rate() == 0)
    g.damage(b, e, 1, clock[0])
    check('被打會醒', 'sleep' not in e.status)
    g.leave_battle(b, p, clock[0])


def test_lose(g):
    print('\n[戰鬥失敗]')
    p = g.by_name['T_bard']
    p.x, p.y = find_spot(g, 12, 18)
    b = controlled_battle(g, p, 'skeleton', 15, tough=False)
    for e in b.alive(1):
        e.atk = e.matk = 9999
        e.spd = 200
    run_until(g, lambda: p.battle is None, 60)
    check('全滅後戰鬥結束', p.battle is None)
    check('傳送回村莊', server.in_town(p.x, p.y))
    check('倒下的寵物剩 1 HP', all(pt['hp'] >= 1 for pt in p.pets))
    check('收到失敗結算', (p.ws.last('bend') or {}).get('win') == 0)


def test_join_and_boss(g):
    print('\n[加入戰鬥 / 炎龍]')
    a, c = g.by_name['T_knight'], g.by_name['T_priest']
    for q in (a, c):
        if q.battle:
            g.leave_battle(g.battles[q.battle], q, clock[0])
        for pt in q.pets:
            d = gd.derive(pt['lv'], pt['st'])
            pt['hp'], pt['mp'] = d['mhp'], d['mmp']
    a.x, a.y = find_spot(g, 12, 18)
    c.x, c.y = a.x, a.y
    b = controlled_battle(g, a, 'poring', 1)
    g.handle(c, {'t': 'bjoin', 'b': b.id})
    check('附近玩家可以加入戰鬥', c.battle == b.id and len(b.pids) == 2 and len(b.alive(0)) == 4)
    for e in b.alive(1):
        e.hp = 1
        e.spd = 0
    pu = b.units[b.pu[c.id]]
    make_ready(pu)
    exp0 = c.exp
    g.handle(c, {'t': 'bcmd', 'u': 'p', 'a': 'atk'})
    run_until(g, lambda: b.over, 10)
    check('勝利後兩個玩家都拿到經驗', c.exp > exp0 and a.battle is None)

    # 炎龍
    bs = g.boss
    a.x, a.y = bs['x'] - 2, bs['y']
    g.handle(a, {'t': 'boss'})
    run_until(g, lambda: a.battle is not None, 10)
    b = battle_of(g, a)
    check('點炎龍開戰', b is not None and b.boss)
    if not b:
        return
    boss = b.alive(1)[0]
    hp1 = boss.mhp
    c.x, c.y = a.x, a.y
    g.handle(c, {'t': 'bjoin', 'b': b.id})
    check('多一人加入,炎龍血量 +1200', boss.mhp == hp1 + gd.BOSS['hp_per_player'])
    check('炎龍戰鬥中地圖上看不到炎龍', g.boss['battle'] == b.id)
    ou = b.units[b.ou[a.id]]
    make_ready(ou)
    g.handle(a, {'t': 'bcmd', 'u': 'o', 'a': 'cap', 'tg': boss.id})
    check('炎龍無法捕捉', boss.alive and any('無法封印' in m for m in a.ws.chats[-3:]))
    run(g, 12)
    check('炎龍會用烈焰吐息', any(f.get('n') == '烈焰吐息' for f in g.fx) or
          any(m.get('t') == 'snap' and any(f.get('n') == '烈焰吐息' for f in m['fx']) for m in a.ws.msgs))
    if a.battle:
        boss.hp = 1
        pu = b.units.get(b.pu.get(a.id))
        if pu and not pu.alive:
            g.revive(b, pu, 1)
        if pu:
            make_ready(pu)
            pu.atk = 99999
            g.handle(a, {'t': 'bcmd', 'u': 'p', 'a': 'atk', 'tg': boss.id})
        run_until(g, lambda: b.over, 10)
    check('打倒炎龍', not g.boss['alive'])
    check('必定掉落幼龍蛋', g.count_item(a, 'egg_drake') + g.count_item(c, 'egg_drake') >= 1)
    check('炎龍擊敗公告', any('炎龍' in m and '擊敗' in m for m in a.ws.chats))
    run(g, gd.BOSS['respawn'] + 1)
    check('3 分鐘後炎龍重生', g.boss['alive'])


def test_hatch_and_pets(g):
    print('\n[孵蛋 / 寵物管理]')
    p = g.by_name['T_priest']
    if p.battle:
        g.leave_battle(g.battles[p.battle], p, clock[0])
    p.x, p.y = 43.5, 48.5   # 孵化屋旁
    p.pets = p.pets[:1]
    p.gold = 5000
    g.handle(p, {'t': 'buy', 'item': 'egg_imp', 'n': 2})
    check('向婆婆買蛋', g.count_item(p, 'egg_imp') == 2 and p.gold == 5000 - 900)
    # 完美照顧 → 12 點
    slot = next(i for i, s in enumerate(p.inv) if s['id'] == 'egg_imp')
    g.handle(p, {'t': 'hstart', 'slot': slot})
    check('開始孵蛋', p.hatch is not None and g.count_item(p, 'egg_imp') == 1)
    ideal = gd.SPECIES['imp']['egg']
    for _ in range(int(gd.HATCH_TIME / server.TICK) + 5):
        h = p.hatch
        if not h:
            break
        h['kt'] = ideal['temp'] - h['ot']
        h['kh'] = ideal['hum'] - h['oh']
        clock[0] += server.TICK
        g.tick()
    pt = p.pets[-1]
    check('完美照顧孵出 12 點極品', pt['sp'] == 'imp' and pt['q'] == 12, pt['q'])
    check('極品公告', any('12 點' in m for m in p.ws.chats))
    check('收到孵化結果', p.ws.last('hatched') is not None)
    # 放著不管
    slot = next(i for i, s in enumerate(p.inv) if s['id'] == 'egg_imp')
    g.handle(p, {'t': 'hstart', 'slot': slot})
    run(g, gd.HATCH_TIME + 1)
    q2 = p.pets[-1]['q']
    check('放著不管 → 素質很差', q2 <= 3, q2)
    # 寵物滿了不能孵
    while len(p.pets) < server.PET_MAX:
        p.pets.append(server.new_pet('poring', 1, 0))
    g.add_item(p, 'egg_dove')
    slot = next(i for i, s in enumerate(p.inv) if s['id'] == 'egg_dove')
    g.handle(p, {'t': 'hstart', 'slot': slot})
    check('寵物滿 5 隻不能孵', p.hatch is None and g.count_item(p, 'egg_dove') == 1)
    # 配點
    pt = server.new_pet('wolf', 5, 0)
    p.pets[1] = pt
    st0, pts0 = list(pt['st']), pt['pts']
    g.handle(p, {'t': 'palloc', 'i': 1, 's': 0, 'n': 3})
    check('手動配點', pt['st'][0] == st0[0] + 3 and pt['pts'] == pts0 - 3)
    g.handle(p, {'t': 'pauto', 'i': 1})
    check('自動配點用完點數', pt['pts'] == 0 and sum(pt['st']) == sum(st0) + pts0)
    g.handle(p, {'t': 'pname', 'i': 1, 'n': '小白'})
    check('改名', pt['n'] == '小白')
    g.handle(p, {'t': 'pset', 'i': 1})
    check('設為出戰', p.active == 1)
    gold = p.gold
    g.handle(p, {'t': 'psell', 'i': 4})
    check('賣寵物給婆婆', len(p.pets) == 4 and p.gold > gold)
    g.handle(p, {'t': 'prelease', 'i': 3})
    check('放生', len(p.pets) == 3)
    # 離線退蛋
    slot = next(i for i, s in enumerate(p.inv) if s['id'] == 'egg_dove')
    g.handle(p, {'t': 'hstart', 'slot': slot})
    g.logout(p)
    data = json.load(open(server.SAVE_FILE, encoding='utf-8'))
    rec = data['T_priest']
    check('離線時孵到一半的蛋退回背包', any(s['id'] == 'egg_dove' for s in rec['inv']))
    p2 = login(g, 'T_priest', 'priest')
    check('重新登入寵物都還在', len(p2.pets) == 3 and p2.pets[1]['n'] == '小白' and p2.active == 1)


def test_wrong_password(g):
    print('\n[帳號]')
    ws = FakeWS()
    check('重複登入被擋', g.login(ws, {'name': 'T_knight', 'pass': 'x', 'cls': 'knight'}) is None)
    g.logout(g.by_name['T_bard'])
    check('密碼錯誤被擋', g.login(ws, {'name': 'T_bard', 'pass': 'wrong'}) is None)


# ============================================================
#  戰鬥平衡模擬:只讓寵物自動戰鬥 (主人不出手),看各區域的勝率與戰鬥時間
# ============================================================
def owner_helps(g, p):
    """簡單的主人策略:牧師在寵物 HP < 45% 時補血,騎士一有空就鼓舞"""
    b = g.battles.get(p.battle)
    if not b:
        return
    ou, pu = b.units.get(b.ou.get(p.id)), b.units.get(b.pu.get(p.id))
    if not g.can_act(ou) or not pu or not pu.alive:
        return
    if p.cls == 'priest' and pu.hp < pu.mhp * 0.45 and ou.mp >= 8:
        g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'oskill', 's': 0, 'tg': pu.id})
    elif p.cls == 'knight' and 'atkup' not in pu.status and ou.mp >= 8:
        g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'oskill', 's': 0, 'tg': pu.id})


def balance(g):
    print('\n[戰鬥平衡模擬] 寵物自動戰鬥,每種情況 60 場')
    setups = [('艾爾文草原', 12, 20, ('poring', 'slime'), 3), ('迷霧森林', 24, 31, ('wolf', 'goblin'), 7),
              ('狼嚎之丘', 33, 39, ('wolf', 'skeleton'), 11), ('亡者荒原', 42, 60, ('skeleton', 'bat'), 15)]
    random.seed(42)
    for zname, dmin, dmax, sps, lv in setups:
        for cls, helps in (('knight', False), ('knight', True), ('priest', True)):
            name = 'B_%s_%d' % (cls, lv)
            p = g.by_name.get(name) or login(g, name, cls)
            wins = rounds = 0
            dur = []
            for i in range(60):
                pt = server.new_pet(sps[i % 2], lv, 4)
                w = [x + 0.2 for x in gd.SPECIES[pt['sp']]['pref']]
                while pt['pts'] > 0:
                    pt['st'][server.wpick(w)] += 1
                    pt['pts'] -= 1
                d = gd.derive(lv, pt['st'])
                pt['hp'], pt['mp'] = d['mhp'], d['mmp']
                p.pets = [pt]
                p.active = 0
                p.lv = lv
                p.recalc()
                p.hp, p.mp = p.mhp, p.mmp
                p.x, p.y = find_spot(g, dmin, dmax)
                p.auto = True
                g.start_encounter(p, clock[0])
                t0 = clock[0]

                def done():
                    if helps:
                        owner_helps(g, p)
                    return p.battle is None
                run_until(g, done, 300)
                end = p.ws.last('bend') or {}
                wins += end.get('win') == 1
                rounds += 1
                dur.append(clock[0] - t0)
            print('  %-6s Lv.%-2d %-3s %-6s 勝率 %3d%%  平均戰鬥 %4.1f 秒' % (
                zname, lv, gd.CLASSES[cls]['name'], '主人協助' if helps else '主人不動',
                wins * 100 // rounds, sum(dur) / len(dur)))


def main():
    g = server.Game()
    test_basics(g)
    test_encounter(g)
    test_capture_swap(g)
    test_class_skills(g)
    test_pet_skills_ai(g)
    test_lose(g)
    test_join_and_boss(g)
    test_hatch_and_pets(g)
    test_wrong_password(g)
    passed = sum(r for _, r in results)
    print('\n%d/%d 通過' % (passed, len(results)))
    if '--balance' in sys.argv:
        balance(g)
    sys.exit(0 if passed == len(results) else 1)


if __name__ == '__main__':
    main()
