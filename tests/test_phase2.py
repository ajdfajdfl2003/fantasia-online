# -*- coding: utf-8 -*-
"""
階段 2 無頭測試:寵物生活(飽食度、快樂值、親密度、餵食、互動、助攻、護主、旅館、離家出走)。
沿用階段 1 的假時鐘與測試工具。

用法:python tests/test_phase2.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_phase1 as T   # noqa: E402  (載入時會把伺服器的時鐘換成假時鐘)
from test_phase1 import check, clock, run, login, controlled_battle, make_ready, find_spot, FakeWS  # noqa: E402

server, gd = T.server, T.gd
CARE = gd.CARE
TOWN = (47.5, 50.5)
KEEPER = (53.5, 51.5)


def near(a, b, tol):
    return abs(a - b) <= tol


def fx_of(g, k):
    return [f for f in g.fx if f['k'] == k]


def fixed_random(seq_value):
    """暫時把 random.random 固定成某個值 (控制機率事件)"""
    orig = server.random.random
    server.random.random = lambda: seq_value
    return orig


# ============================================================
def test_start_values(g):
    print('\n[起始值與舊存檔]')
    p = login(g, 'C_new', 'knight')
    pt = p.pets[0]
    check('新手噗噗 飽食80 快樂70 親密20', (pt['food'], pt['joy'], pt['bond']) == (80, 70, 20))
    # 孵化
    p.x, p.y = 42.5, 49.5
    g.add_item(p, 'egg_fox')
    slot = next(i for i, s in enumerate(p.inv) if s['id'] == 'egg_fox')
    g.hatch_start(p, slot, clock[0])
    run(g, gd.HATCH_TIME + 1)
    hp = p.pets[-1]
    check('孵化的寵物 飽食70 快樂80 親密30', hp['sp'] == 'fox' and near(hp['food'], 70, 0.1) and near(hp['joy'], 80, 0.1)
          and hp['bond'] == 30, (hp['food'], hp['joy'], hp['bond']))
    # 捕捉 (固定成功)
    p.x, p.y = TOWN
    b = controlled_battle(g, p, 'wolf', 2)
    ou = b.units[b.ou[p.id]]
    make_ready(ou)
    tg = b.alive(1)[0]
    orig = fixed_random(0.0)
    try:
        g.capture(b, p, ou, tg, clock[0])
    finally:
        server.random.random = orig
    cp = p.pets[-1]
    check('捕捉的寵物 飽食50 快樂40 親密0~10', cp['sp'] == 'wolf' and cp['food'] == 50 and cp['joy'] == 40 and 0 <= cp['bond'] <= 10)
    g.leave_battle(b, p, clock[0])
    # 舊存檔 (階段 1 沒有照顧數值)
    old = server.new_pet('slime', 3, 2)
    for k in ('food', 'joy', 'bond', 'sync'):
        old.pop(k)
    salt = 'abc'
    g.accounts['C_old'] = {'salt': salt, 'hash': server.hash_pw(salt, 'x'), 'cls': 'mage', 'lv': 2, 'exp': 0,
                           'gold': 50, 'inv': [], 'pets': [old], 'active': 0, 'x': TOWN[0], 'y': TOWN[1],
                           'last': int(clock[0])}
    q = g.login(FakeWS(), {'name': 'C_old', 'pass': 'x'})
    o = q.pets[0]
    check('舊存檔補上照顧數值 (80/70/15)', (o['food'], o['joy'], o['bond'], o['sync']) == (80, 70, 15, 0))
    check('舊存檔沒有 bank 也能登入', q.bank == [])


def test_decay(g):
    print('\n[飽食度與快樂值的消耗]')
    p = login(g, 'C_decay', 'priest')
    p.x, p.y = TOWN
    p.pets.append(server.new_pet('wolf', 3, 3))
    a, o = p.pets
    for pt in (a, o):
        pt['food'], pt['joy'] = 100.0, 100.0
    p.bank.append(server.new_pet('fox', 3, 3))
    bk = p.bank[0]
    bk['food'], bk['joy'] = 50.0, 20.0
    run(g, 1200)   # 20 分鐘
    check('出戰寵物每小時 −15 (20 分鐘 −5)', near(a['food'], 95, 0.3), a['food'])
    check('其他寵物每小時 −7.5 (20 分鐘 −2.5)', near(o['food'], 97.5, 0.3), o['food'])
    check('快樂值每小時 −6 (20 分鐘 −2)', near(a['joy'], 98, 0.3), a['joy'])
    check('旅館裡的寵物飽食度不變', bk['food'] == 50, bk['food'])
    check('旅館裡的寵物快樂值每小時 +60', near(bk['joy'], 40, 0.5), bk['joy'])
    # 肚子餓、餓昏
    a['food'], a['joy'] = 30.05, 80.0
    p.ws.chats.clear()
    run(g, 60)
    check('跨過 30 時通知「肚子餓了」', any('肚子餓了' in c for c in p.ws.chats))
    check('肚子餓時快樂值下降加快', a['joy'] < 80 - 0.9, a['joy'])
    a['food'], a['bond'] = 0.002, 50.0
    run(g, 2)
    check('飽食度歸零 → 餓昏通知、親密度 −2', a['food'] == 0 and a['bond'] == 48 and any('餓昏' in c for c in p.ws.chats))
    check('餓昏的寵物不能戰鬥', not server.can_fight(a))


def test_offline(g):
    print('\n[離線暫停]')
    p = login(g, 'C_off', 'bard')
    p.x, p.y = TOWN
    pt = p.pets[0]
    pt['food'], pt['joy'] = 60.0, 60.0
    g.logout(p)
    clock[0] += 10 * 3600
    p = g.login(FakeWS(), {'name': 'C_off', 'pass': 'x'})
    pt = p.pets[0]
    check('離線 10 小時,飽食度與快樂值不變', pt['food'] == 60 and pt['joy'] == 60, (pt['food'], pt['joy']))
    check('離線不到一天沒有「想你」', not any('想你' in c for c in p.ws.chats))
    g.logout(p)
    clock[0] += 25 * 3600
    p = g.login(FakeWS(), {'name': 'C_off', 'pass': 'x'})
    check('離線超過一天,寵物撲過來說想你', any('想你' in c for c in p.ws.chats) and fx_of(g, 'pact'))


def test_feed(g):
    print('\n[餵食]')
    p = login(g, 'C_feed', 'knight')
    p.x, p.y = TOWN
    pt = p.pets[0]   # 噗噗:最愛莓果、討厭木材
    for f in ('berry', 'wood', 'meat'):
        g.add_item(p, f, 3)
    pt['food'], pt['joy'], pt['bond'] = 40.0, 50.0, 10.0
    g.feed(p, 0, 'berry', clock[0])
    check('最愛:飽食+35 快樂+10 親密+4', (pt['food'], pt['joy'], pt['bond']) == (75, 60, 14), (pt['food'], pt['joy'], pt['bond']))
    pt['food'] = 40.0
    g.feed(p, 0, 'meat', clock[0])
    check('普通:飽食+30 快樂+2 親密+0', (pt['food'], pt['joy'], pt['bond']) == (70, 62, 14))
    pt['food'] = 40.0
    g.feed(p, 0, 'wood', clock[0])
    check('討厭:飽食+15 快樂−8', (pt['food'], pt['joy']) == (55, 54))
    pt['food'] = 95.0
    n = g.count_item(p, 'berry')
    g.feed(p, 0, 'berry', clock[0])
    check('飽食度 ≥ 90 吃不下,食物不會被吃掉', g.count_item(p, 'berry') == n and pt['food'] == 95)
    # 史萊姆雜食
    p.pets.append(server.new_pet('slime', 2, 2))
    sl = p.pets[1]
    sl['food'], sl['joy'], sl['bond'] = 40.0, 50.0, 0.0
    g.feed(p, 1, 'meat', clock[0])
    check('綠史萊姆雜食:每種都「喜歡」(+30/+5/+2)', (sl['food'], sl['joy'], sl['bond']) == (70, 55, 2))
    # 餓昏後餵食就能戰鬥
    pt['food'] = 0.0
    g.feed(p, 0, 'berry', clock[0])
    check('餓昏的寵物吃東西後可以戰鬥', server.can_fight(pt))
    # 背包雙擊食物 = 餵出戰寵物
    pt['food'] = 40.0
    slot = next(i for i, s in enumerate(p.inv) if s['id'] == 'berry')
    g.use_item(p, slot, None)
    check('背包雙擊食物餵出戰寵物', pt['food'] == 75)
    # 戰鬥中不能餵
    b = controlled_battle(g, p)
    pt['food'] = 40.0
    g.feed(p, 0, 'berry', clock[0])
    check('戰鬥中不能餵食', pt['food'] == 40)
    g.leave_battle(b, p, clock[0])
    check('食物在道具商店有賣', all(f in gd.SHOP_ITEMS for f in gd.FOODS))


def test_interact(g):
    print('\n[互動動作]')
    p = login(g, 'C_int', 'hunter')
    p.x, p.y = TOWN
    pt = p.pets[0]
    pt['food'], pt['joy'], pt['bond'] = 60.0, 50.0, 10.0
    g.pet_interact(p, 0, 'pet', clock[0])
    check('摸摸:快樂+5 親密+0.5', (pt['joy'], pt['bond']) == (55, 10.5))
    g.pet_interact(p, 0, 'pet', clock[0])
    check('摸摸冷卻中:數值不變但有反應', (pt['joy'], pt['bond']) == (55, 10.5) and fx_of(g, 'pact')[-1]['r'] == 'cd')
    clock[0] += 181
    g.pet_interact(p, 0, 'pet', clock[0])
    check('冷卻 3 分鐘後可以再摸', pt['joy'] == 60)
    g.pet_interact(p, 0, 'play', clock[0])
    check('玩耍:快樂+15 親密+1 飽食−5', (pt['joy'], pt['bond'], pt['food']) == (75, 12, 55))
    pt['food'] = 5.0
    clock[0] += 601
    g.pet_interact(p, 0, 'play', clock[0])
    check('飽食度不到 10 不能玩耍', pt['joy'] == 75)
    g.fx.clear()
    g.pet_interact(p, 0, 'trick', clock[0])
    check('親密度不到 50 不肯表演', not fx_of(g, 'pact'))
    pt['bond'] = 50.0
    g.pet_interact(p, 0, 'trick', clock[0])
    check('親密度 50 可以表演,附近玩家看得到', fx_of(g, 'pact') and fx_of(g, 'pact')[-1]['a'] == 'trick')
    g.pet_interact(p, 0, 'pet', clock[0])
    j, uid = pt['joy'], pt['uid']
    g.logout(p)
    p = g.login(FakeWS(), {'name': 'C_int', 'pass': 'x'})
    p.x, p.y = TOWN
    pt = p.pets[0]
    g.pet_interact(p, 0, 'pet', clock[0])
    check('重新登入不會重置互動冷卻 (不能靠重登刷親密度)', pt['uid'] == uid and pt['joy'] == j)
    b = controlled_battle(g, p)
    j = pt['joy']
    clock[0] += 999
    g.pet_interact(p, 0, 'pet', clock[0])
    check('戰鬥中不能互動', pt['joy'] == j)
    g.leave_battle(b, p, clock[0])


def test_hunger_combat(g):
    print('\n[餓昏與肚子餓的戰鬥影響]')
    p = login(g, 'C_hun', 'knight')
    p.pets.append(server.new_pet('wolf', 3, 3))
    p.x, p.y = find_spot(g, 12, 18)
    for pt in p.pets:
        pt['food'] = 0.0
    check('全部餓昏 → 沒有能出戰的寵物', p.alive_pet() is None)
    p.steps = 99
    g.encounter_check(p, 50, clock[0])
    check('全部餓昏時不會遇敵', p.battle is None)
    p.pets[1]['food'] = 50.0
    check('出戰寵物餓昏時,改派其他寵物', p.alive_pet() == 1)
    p.pets[0]['food'], p.pets[1]['food'] = 50.0, 0.0
    b = controlled_battle(g, p)
    ou = b.units[b.ou[p.id]]
    make_ready(ou)
    g.swap_pet(b, p, ou, 1, clock[0])
    check('不能換上餓昏的寵物', b.units[b.pu[p.id]].pet is p.pets[0])
    g.leave_battle(b, p, clock[0])
    pt = p.pets[0]
    pt['food'] = 80.0
    full = g.pet_unit(p, 0)
    pt['food'] = 20.0
    hungry = g.pet_unit(p, 0)
    check('肚子餓時攻擊、防禦 ×0.9', hungry.atk == int(full.atk * 0.9) and hungry.df == int(full.df * 0.9),
          (full.atk, hungry.atk))


def test_disobey(g):
    print('\n[心情差不聽指令]')
    p = login(g, 'C_dis', 'knight')
    p.x, p.y = TOWN
    pt = p.pets[0]
    pt['food'] = 80.0

    def rate(joy, bond, n=600):
        pt['joy'], pt['bond'] = float(joy), float(bond)
        b = controlled_battle(g, p)
        pu = b.units[b.pu[p.id]]
        cnt = 0
        for _ in range(n):
            make_ready(pu)
            g.fx.clear()
            g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'atk'})
            cnt += bool(fx_of(g, 'disobey'))
            pt['joy'], pt['bond'] = float(joy), float(bond)
        g.leave_battle(b, p, clock[0])
        return cnt / float(n)
    r0 = rate(5, 0)
    check('快樂值 < 10、親密度 0:約 30% 不聽', 0.24 <= r0 <= 0.36, r0)
    r1 = rate(20, 0)
    check('快樂值 < 30:約 15% 不聽', 0.10 <= r1 <= 0.20, r1)
    r2 = rate(5, 100)
    check('親密度 100 時機率減半 (約 15%)', 0.10 <= r2 <= 0.20, r2)
    r3 = rate(60, 0, 200)
    check('心情好時一定聽話', r3 == 0, r3)


def test_assist(g):
    print('\n[助攻 A:技能加成]')
    pk = login(g, 'C_kn', 'knight')
    pp = login(g, 'C_pr', 'priest')
    for q in (pk, pp):
        q.x, q.y = TOWN
        q.lv = 6
        q.recalc()
        q.mp = q.mmp
    b = controlled_battle(g, pk)
    g.join_battle(b, pp, clock[0])
    ku, pu2 = b.units[b.pu[pk.id]], b.units[b.pu[pp.id]]
    kou, pou = b.units[b.ou[pk.id]], b.units[b.ou[pp.id]]
    ku.pet['bond'] = 100.0
    pu2.pet['bond'] = 100.0
    make_ready(kou)
    g.owner_skill(b, pk, kou, 0, ku, clock[0])   # 鼓舞自己的寵物
    check('鼓舞自己的寵物 (親密度 100):攻擊 +45%', near(server.smod(ku, 'atkup', 1.3), 1.45, 1e-6), server.smod(ku, 'atkup', 1.3))
    check('發動時冒「助攻 +50%」', any(f.get('v') == 50 for f in fx_of(g, 'boost')))
    make_ready(kou)
    g.owner_skill(b, pk, kou, 0, pu2, clock[0])  # 鼓舞別人的寵物
    check('用在別人的寵物上沒有加成', near(server.smod(pu2, 'atkup', 1.3), 1.3, 1e-6))
    # 治癒術
    heal = {}
    for bond in (0, 100):
        pu2.pet['bond'] = float(bond)
        pu2.hp = 1
        make_ready(pou)
        g.owner_skill(b, pp, pou, 0, pu2, clock[0])
        heal[bond] = pu2.hp - 1
    check('治癒術回復量:親密度 100 是 0 的 1.5 倍', near(heal[100] / float(heal[0]), 1.5, 0.05), heal)
    g.leave_battle(b, pp, clock[0])
    g.leave_battle(b, pk, clock[0])


def test_sync(g):
    print('\n[助攻 B:默契與助攻指令]')
    p = login(g, 'C_sync', 'mage')
    p.x, p.y = TOWN
    pt = p.pets[0]
    pt['food'], pt['joy'], pt['bond'], pt['sync'] = 80.0, 80.0, 30.0, 0.0
    b = controlled_battle(g, p)
    pu = b.units[b.pu[p.id]]
    make_ready(pu)
    g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'atk'})
    check('親密度 < 40 不累積默契', pu.sync == 0)
    pu.sync = 100
    g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'assist'})
    check('親密度 < 40 不能助攻', not pu.surge)
    g.leave_battle(b, p, clock[0])
    pt['bond'], pt['sync'] = 100.0, 0.0
    b = controlled_battle(g, p)
    pu = b.units[b.pu[p.id]]
    make_ready(pu)
    g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'atk'})
    check('親密度 100:行動一次默契 +9 (6 × 1.5)', near(pu.sync, 9, 1e-6), pu.sync)
    e = b.alive(1)[0]
    g.damage(b, pu, 10, clock[0])
    check('被打一次默契 +6 (4 × 1.5)', near(pu.sync, 15, 1e-6), pu.sync)
    g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'assist'})
    check('默契不到 100 不能助攻', not pu.surge)
    # 固定亂數,比較一般攻擊與助攻後的傷害
    ou = server.random.uniform
    orig = fixed_random(0.5)
    server.random.uniform = lambda a, b: (a + b) / 2.0
    try:
        make_ready(pu)
        h = e.hp
        g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'atk', 'tg': e.id})
        normal = h - e.hp
        pu.sync = 100
        pu.bar, pu.ready_at = 10, None
        g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'assist'})
        check('助攻:不用等主人時間棒,寵物立刻可以行動', pu.surge and pu.ready_at is not None and pu.sync == 0)
        h = e.hp
        g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'atk', 'tg': e.id})
        boosted = h - e.hp
        check('助攻後的攻擊威力約 ×1.5', boosted > normal * 1.3, (normal, boosted))
        pu.sync = 100
        g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'assist'})
        mp = pu.mp
        sk = pu.skills[0]
        g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'skill', 's': sk, 'tg': e.id})
        check('助攻後的技能不耗 MP', pu.mp == mp and not pu.surge, (mp, pu.mp))
        pt['joy'] = 0.0
        pu.sync = 100
        make_ready(pu)
        g.handle(p, {'t': 'bcmd', 'u': 'o', 'a': 'assist'})
        g.fx.clear()
        g.handle(p, {'t': 'bcmd', 'u': 'p', 'a': 'atk', 'tg': e.id})
        check('助攻後一定聽話', not fx_of(g, 'disobey'))
    finally:
        server.random.random = orig
        server.random.uniform = ou
    pu.sync = 42
    g.leave_battle(b, p, clock[0])
    check('默契量表跨戰鬥保留', pt['sync'] == 42)
    pt['joy'] = 80.0


def test_protect(g):
    print('\n[護主]')
    p = login(g, 'C_pro', 'knight')
    p.x, p.y = TOWN
    pt = p.pets[0]
    pt['food'], pt['joy'] = 80.0, 80.0
    b = controlled_battle(g, p)
    pu, ou = b.units[b.pu[p.id]], b.units[b.ou[p.id]]
    for bond, want in ((0, 15), (100, 5)):
        pt['bond'] = float(bond)
        ou.hp = ou.mhp
        pu.hp = pu.mhp = 9999
        g.damage(b, pu, 100, clock[0])
        check('連動傷害:親密度 %d → %d%%' % (bond, want), ou.mhp - ou.hp == want, ou.mhp - ou.hp)
    pt['bond'] = 50.0
    ou.hp = int(ou.mhp * 0.25)
    run(g, 0.1)
    check('親密度 < 60 不會護主', 'protect' not in pu.status)
    pt['bond'] = 60.0
    run(g, 0.1)
    check('主人 HP < 30% → 寵物進入護主姿態', 'protect' in pu.status)
    h = ou.hp
    g.damage(b, pu, 200, clock[0])
    check('護主時主人不會被連動扣血', ou.hp == h)
    check('護主時寵物防禦 ×1.3', near(server.smod(pu, 'protect', CARE['guard_def']), 1.3, 1e-6))
    ou.hp = int(ou.mhp * 0.6)
    run(g, 0.1)
    check('主人 HP 回到 50% 以上 → 結束護主', 'protect' not in pu.status)
    g.leave_battle(b, p, clock[0])


def test_battle_care(g):
    print('\n[戰鬥後的照顧數值]')
    p = login(g, 'C_bc', 'priest')
    p.x, p.y = TOWN
    pt = p.pets[0]
    pt['food'], pt['joy'], pt['bond'] = 80.0, 50.0, 10.0
    b = controlled_battle(g, p, tough=False)
    for e in b.alive(1):
        g.ko(b, e, clock[0])
    g.check_end(b, clock[0])
    check('打贏:上場的寵物 飽食−0.5、快樂+1、親密+0.05',
          near(pt['food'], 79.5, 0.05) and near(pt['joy'], 51, 0.05) and near(pt['bond'], 10.05, 1e-6),
          (pt['food'], pt['joy'], pt['bond']))
    b = controlled_battle(g, p)
    pu = b.units[b.pu[p.id]]
    j, bd = pt['joy'], pt['bond']
    g.ko(b, pu, clock[0])
    check('寵物倒下:快樂−5、親密−1', near(pt['joy'], j - 5, 0.01) and near(pt['bond'], bd - 1, 1e-6))
    j = pt['joy']
    g.ko(b, b.units[b.ou[p.id]], clock[0])
    g.check_end(b, clock[0])
    check('打輸:快樂−10', near(pt['joy'], j - 10, 0.05), (j, pt['joy']))
    # 升級
    pt['joy'] = 40.0
    g.give_pet_exp(p, pt, server.exp_need(pt['lv']))
    check('寵物升級:快樂+10', near(pt['joy'], 50, 1e-6))
    # 食物掉落
    random.seed(7)
    drops = 0
    for _ in range(400):
        bb = server.Battle(0, 0, 0)
        u = g.wild_unit('wolf', 3)
        bb.add(u)
        g.ko(bb, u, clock[0])
        drops += bb.loot.count('meat')
    check('野狼約 25% 掉落最愛的鮮肉', 0.19 <= drops / 400.0 <= 0.31, drops / 400.0)
    bb = server.Battle(0, 0, 0)
    got = set()
    for _ in range(200):
        u = g.wild_unit('slime', 3)
        bb.add(u)
        g.ko(bb, u, clock[0])
    got = {x for x in bb.loot if x in gd.FOODS}
    check('綠史萊姆掉落隨機食物', len(got) >= 4, got)


def test_bank(g):
    print('\n[寵物旅館]')
    p = login(g, 'C_bank', 'bard')
    p.pets.append(server.new_pet('wolf', 3, 3))
    p.x, p.y = TOWN
    g.bank_put(p, 1)
    check('離旅館太遠不能寄放', len(p.pets) == 2)
    p.x, p.y = KEEPER
    p.pets[1]['hp'] = 1
    g.bank_put(p, 1)
    check('寄放成功,HP 補滿', len(p.pets) == 1 and len(p.bank) == 1 and p.bank[0]['hp'] == gd.derive(3, p.bank[0]['st'])['mhp'])
    g.bank_put(p, 0)
    check('身上至少留一隻', len(p.pets) == 1)
    for _ in range(gd.CARE['bank_max'] - 1):
        p.pets.append(server.new_pet('poring', 1, 0))
        g.bank_put(p, 1)
    p.pets.append(server.new_pet('poring', 1, 0))
    g.bank_put(p, 1)
    check('旅館最多 20 隻', len(p.bank) == 20 and len(p.pets) == 2, len(p.bank))
    while len(p.pets) < server.PET_MAX:
        p.pets.append(server.new_pet('poring', 1, 0))
    g.bank_get(p, 0)
    check('身上滿 5 隻不能領回', len(p.pets) == server.PET_MAX and len(p.bank) == 20)
    p.pets = p.pets[:1]
    p.active = 0
    g.bank_get(p, 0)
    check('領回成功', len(p.pets) == 2 and p.pets[1]['sp'] == 'wolf' and len(p.bank) == 19)
    run(g, 1)
    m = p.ws.last('bank')
    check('送出旅館清單給客戶端', m and len(m['bank']) == 19 and m['max'] == 20)
    g.logout(p)
    p = g.login(FakeWS(), {'name': 'C_bank', 'pass': 'x'})
    check('旅館的寵物會存檔', len(p.bank) == 19)
    g.npc_action(p, 6, 'bank', {}) if server.dist(p.x, p.y, 53.5, 50.5) <= 4 else None
    check('旅館 NPC 開啟旅館視窗', p.ws.last('bankui') is not None)


def test_sulk(g):
    print('\n[離家出走]')
    p = login(g, 'C_sulk', 'knight')
    p.pets.append(server.new_pet('wolf', 3, 3))
    p.x, p.y = TOWN
    a = p.pets[0]
    a['food'], a['joy'], a['bond'] = 0.0, 0.0, 30.0
    p.ws.chats.clear()
    run(g, 310)
    check('快樂與飽食都是 0 持續 5 分鐘 → 警告', any('受不了' in c for c in p.ws.chats) and len(p.pets) == 2)
    b = controlled_battle(g, p)
    s = p.sulk.get(a['uid'], 0)
    run(g, 400)
    check('戰鬥中不累積離家出走時間', p.sulk.get(a['uid'], 0) <= s + 1e-6)
    g.leave_battle(b, p, clock[0])
    a['food'], a['joy'] = 0.0, 0.0
    run(g, 320)
    check('持續 10 分鐘 → 跑去寵物旅館', a not in p.pets and a in p.bank and a['sulk'])
    check('出走時親密度 −10、旅館餵到 %d (不會一領回就肚子餓)' % CARE['sulk_food'],
          near(a['bond'], 20, 1e-6) and a['food'] >= CARE['sulk_food'] > CARE['hungry'], (a['bond'], a['food']))
    check('出戰寵物索引修正', p.active == 0 and p.pets[0]['sp'] == 'wolf')
    # 旅館滿了也收、最後一隻也可能出走
    for _ in range(20):
        p.bank.append(server.new_pet('poring', 1, 0))
    w = p.pets[0]
    w['food'], w['joy'] = 0.0, 0.0
    run(g, 601)
    check('旅館滿了也收,最後一隻也會出走', not p.pets and w in p.bank)
    p.x, p.y = find_spot(g, 12, 18)
    p.steps = 99
    g.encounter_check(p, 50, clock[0])
    run(g, 2)
    check('身上沒有寵物:不會遇敵、不會出錯', p.battle is None and p.ws.last('snap') is not None)
    p.x, p.y = KEEPER
    i = p.bank.index(a)
    p.ws.chats.clear()
    g.bank_get(p, i)
    check('到旅館帶回賭氣的寵物', a in p.pets and not a['sulk'])
    check('還在鬧脾氣:蘿絲提醒要多陪牠 (不說「不生氣了」)', a['joy'] < CARE['angry'] and any('還在生悶氣' in c for c in p.ws.chats))
    p.remove_pet(p.pets.index(a))   # 再賭氣一次,這次在旅館住到心情變好
    p.bank.append(a)
    a['sulk'], a['joy'] = True, 50.0
    p.ws.chats.clear()
    g.bank_get(p, p.bank.index(a))
    check('旅館住到心情變好:蘿絲說牠不生氣了', any('不生氣了' in c for c in p.ws.chats))


def test_moods(g):
    print('\n[心情泡泡]')
    pt = server.new_pet('poring', 1, 0)
    cases = [((0, 50, 50, 0), 'starve'), ((20, 50, 50, 0), 'hungry'), ((60, 20, 50, 0), 'angry'),
             ((60, 50, 50, 25), 'sleepy'), ((60, 90, 70, 0), 'love'), ((60, 60, 30, 0), '')]
    for (food, joy, bond, idle), want in cases:
        pt['food'], pt['joy'], pt['bond'] = float(food), float(joy), float(bond)
        check('泡泡 %-6s (飽食%d 快樂%d 親密%d 發呆%d秒)' % (want or '(無)', food, joy, bond, idle),
              server.pet_mood(pt, idle) == want, server.pet_mood(pt, idle))
    p = login(g, 'C_mood', 'knight')
    p.x, p.y = TOWN
    p.pets[0]['food'] = 20.0
    run(g, 0.2)
    me = next(e for e in p.ws.last('snap')['e'] if e['i'] == p.id)
    check('地圖快照帶有跟隨寵物的心情', me.get('pm') == 'hungry', me.get('pm'))
    p.pets[0]['food'] = 80.0
    p.pets[0]['joy'] = 80.0
    b = controlled_battle(g, p, 'wolf', 12)
    run(g, 0.2)
    snap = p.ws.last('snap')
    mine = [u for bt in snap['bt'] for u in bt['u'] if u['k'] == 'p' and u['pid'] == p.id]
    check('遇到高 5 級以上的敵人會害怕發抖', mine and mine[0].get('md') == 'scared', mine and mine[0].get('md'))
    g.leave_battle(b, p, clock[0])


def test_art():
    print('\n[圖片管線:清單與存檔規則]')
    orig = server.ASSETS
    server.ASSETS = os.path.join(T.TMP, 'assets')
    try:
        m = server.asset_manifest()
        check('沒有圖時清單是空的,帶有顯示大小', m['files'] == [] and m['art']['poring']['size'] == gd.ART['poring']['size']
              and 'dragon' in m['species'])
        webp = b'RIFF\x10\x00\x00\x00WEBPVP8 fake-body'   # 階段 4 起成品改存 WebP
        ok, _ = server.save_art('pets/poring.webp', webp)
        ok2, _ = server.save_art('pets/imp_attack.webp', webp)
        ok3, _ = server.save_art('npcs/keeper.webp', webp)
        check('可以存主圖、動作圖、NPC 圖', ok and ok2 and ok3)
        m = server.asset_manifest()
        check('清單列出存好的圖', sorted(f['p'] for f in m['files']) == ['npcs/keeper.webp', 'pets/imp_attack.webp', 'pets/poring.webp'])
        bad = ['pets/../server.py', 'pets/unknown.webp', 'pets/poring_dance.webp', 'other/poring.webp', 'pets/poring.jpg',
               '../poring.webp', 'pets/sub/poring.webp', 'npcs/nobody.webp', 'pets/poring.png']
        check('不符規格的檔名一律拒絕', all(server.art_path(n) is None for n in bad), [n for n in bad if server.art_path(n)])
        ok, _ = server.save_art('pets/slime.webp', b'not a webp')
        check('不是 WebP 的資料拒絕', not ok and not os.path.exists(os.path.join(server.ASSETS, 'pets', 'slime.webp')))
        ok, _ = server.save_art('pets/poring.webp', b'', delete=True)
        check('可以刪除圖片 (退回程式繪圖)', ok and not os.path.exists(os.path.join(server.ASSETS, 'pets', 'poring.webp')))
        # art-src/:使用者放原圖的地方,只列出圖片檔
        orig_src = server.ART_SRC
        server.ART_SRC = os.path.join(T.TMP, 'art-src')
        os.makedirs(server.ART_SRC, exist_ok=True)
        for fn in ('噗噗.png', '小火妖_攻擊.jpg', 'notes.txt'):
            open(os.path.join(server.ART_SRC, fn), 'wb').write(b'x')
        check('art-src 只列出圖片 (中文檔名也可以)', server.src_files() == ['噗噗.png', '小火妖_攻擊.jpg'] or
              sorted(server.src_files()) == sorted(['噗噗.png', '小火妖_攻擊.jpg']), server.src_files())
        check('清單帶有 art-src 的原圖', sorted(server.asset_manifest()['src']) == sorted(['噗噗.png', '小火妖_攻擊.jpg']))
        server.ART_SRC = orig_src
    finally:
        server.ASSETS = orig


def main():
    test_art()
    g = server.Game()
    test_start_values(g)
    test_decay(g)
    test_offline(g)
    test_feed(g)
    test_interact(g)
    test_hunger_combat(g)
    test_disobey(g)
    test_assist(g)
    test_sync(g)
    test_protect(g)
    test_battle_care(g)
    test_bank(g)
    test_sulk(g)
    test_moods(g)
    passed = sum(r for _, r in T.results)
    print('\n%d/%d 通過' % (passed, len(T.results)))
    sys.exit(0 if passed == len(T.results) else 1)


if __name__ == '__main__':
    main()
