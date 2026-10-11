# -*- coding: utf-8 -*-
"""
階段 3 無頭測試:繁殖與進化(技能升階、專屬技能、新的技能效果、進化、發情、配對、配對蛋、混種、存檔)。
沿用階段 1 的假時鐘與測試工具。

用法:python tests/test_phase3.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_phase1 as T   # noqa: E402  (載入時會把伺服器的時鐘換成假時鐘)
from test_phase1 import check, clock, run, login, controlled_battle, make_ready, FakeWS  # noqa: E402

server, gd = T.server, T.gd
SP, CARE, BREED, EVOLVE = gd.SPECIES, gd.CARE, gd.BREED, gd.EVOLVE
HATCHER = (42.5, 49.5)


def fx_of(g, k):
    return [f for f in g.fx if f['k'] == k]


def bfx_of(g, k):
    return [f for f in g.fx if f.get('b') is not None and f['k'] == k]


def fixed_random(v):
    orig = server.random.random
    server.random.random = lambda: v
    return orig


def mkpet(sp, lv, q=6, joy=90.0, bond=70.0, food=80.0):
    pt = server.new_pet(sp, lv, q)
    pt['joy'], pt['bond'], pt['food'] = joy, bond, food
    return pt


def battle_with(g, p, foes):
    """開一場可控制的戰鬥,foes = [(種族, 等級)];敵人血很多、不會行動"""
    b = g.new_battle(p.x, p.y)
    g.add_player(b, p, clock[0])
    for sp, lv in foes:
        u = g.wild_unit(sp, lv)
        u.mhp = u.hp = 99999
        u.spd = 0
        b.add(u)
    g.restack(b)
    return b


# ============================================================
def test_data():
    print('\n[資料:進化型態、技能線、混種]')
    lines = [k for k, v in SP.items() if v['stage'] == 0]
    check('13 個種族系 × 3 階 = 39 個種族', len(lines) == 13 and len(SP) == 39)
    check('全部種族的技能都有定義', all(s in gd.PET_SKILLS for v in SP.values() for s, _ in v['skills']))
    check('進化鏈:poring → poring2 → poring3 → 最終', SP['poring']['evo'] == 'poring2' and SP['poring2']['evo'] == 'poring3'
          and SP['poring3']['evo'] is None)
    check('進化型態的代號沒有底線 (底線留給動作圖)', all('_' not in k for k in SP))
    check('中階能力 = 初階 ×1.25,每級點數 +1', SP['poring2']['base'] == (19, 18, 11, 15) and SP['poring2']['grow'] == 5)
    check('高階能力 = 初階 ×1.5,每級點數 +2', SP['wolf3']['base'] == (27, 20, 12, 26) and SP['wolf3']['grow'] == 6)
    check('進化型態野外抓不到、沒有賣蛋', all(v['cap'] == 0 and 'egg' not in v for v in SP.values() if v['stage']))
    check('混種只能靠配對 (不能捕捉、野外沒有)', SP['silverwolf']['cap'] == 0 and
          not any(m[0] in ('silverwolf', 'duskbird') for z in gd.ZONES for m in z['mobs'] + [z['rare']]))
    check('每個種族系都能孵 (有溫濕度)', all(gd.hatch_pref(k) for k in lines))
    check('野狼、彩虹鴿的 Lv.10 技能換掉了', SP['wolf']['skills'][2][0] == 'bite' and SP['dove']['skills'][2][0] == 'heal')
    check('種族技能線都有中階、高階', all(s in gd.SKILL_TIERS for k in lines for s, _ in SP[k]['skills']))
    check('顯示大小:中階 ×1.15、高階 ×1.3', gd.ART['poring2']['size'] == 39 and gd.ART['wolf3']['size'] == 78
          and gd.ART['imp2'].get('hover') == gd.ART['imp']['hover'])
    check('技能清單:初階 Lv.10', gd.pet_skills('poring', 10) == ['tackle', 'heal', 'quake'])
    check('技能清單:中階升階 + 專屬技能', gd.pet_skills('poring2', 10) == ['strike', 'heal2', 'quake2', 'jellyeat'])
    check('技能清單:遺傳技能跟著階段升階', gd.pet_skills('poring3', 30, 'sleep')[-1] == 'sleep3'
          and gd.pet_skills('poring', 1, 'sleep') == ['tackle', 'sleep'])
    check('可遺傳的技能不含專屬技能', gd.inheritable('wolf2', 'sleep') == ['double', 'gale', 'bite', 'sleep'])


def test_skills(g):
    print('\n[技能效果:我方全體、全體吸血、附加狀態、偷金幣]')
    a = login(g, 'S_a', 'knight')
    c = login(g, 'S_c', 'priest')
    a.pets = [mkpet('wolf2', 12)]
    c.pets = [mkpet('poring', 10)]
    a.x, a.y = c.x, c.y = 47.5, 50.5
    b = battle_with(g, a, [('slime', 5), ('goblin', 6)])
    g.join_battle(b, c, clock[0])
    pa, pc = b.units[b.pu[a.id]], b.units[b.pu[c.id]]
    check('戰鬥快照帶有自己寵物的技能清單 (含專屬)', 'howl' in g.unit_view(pa, clock[0], b)['sk'])
    orig = fixed_random(0.0)
    try:
        make_ready(pa)
        g.battle_cmd(a, {'u': 'p', 'a': 'skill', 's': 'howl'}, clock[0])
        check('狼嚎:我方全體寵物攻擊力提升', 'atkup' in pa.status and 'atkup' in pc.status)
        foes = b.alive(1)
        u = b.units[b.pu[a.id]]
        u.skills.append('curse')
        make_ready(u)
        u.mp = 99
        g.battle_cmd(a, {'u': 'p', 'a': 'skill', 's': 'curse'}, clock[0])
        check('亡者詛咒:全體敵人攻擊力下降', all('atkdown' in f.status for f in foes))
        u.skills.append('firedance')
        make_ready(u)
        u.mp = 99
        g.battle_cmd(a, {'u': 'p', 'a': 'skill', 's': 'firedance'}, clock[0])
        check('火妖之舞:全體攻擊並灼傷 (中毒)', all('poison' in f.status and f.hp < f.mhp for f in foes))
        server.random.random = lambda: 0.99   # 物理攻擊:不會閃避、不會爆擊
        u.skills.append('feast')
        make_ready(u)
        u.mp, u.hp = 99, 1
        g.battle_cmd(a, {'u': 'p', 'a': 'skill', 's': 'feast'}, clock[0])
        check('血之盛宴:全體攻擊並吸血', u.hp > 1)
        pc.hp = 1
        u.skills.append('heal3')
        make_ready(u)
        u.mp = 99
        g.battle_cmd(a, {'u': 'p', 'a': 'skill', 's': 'heal3'}, clock[0])
        check('群體治療術:我方全體寵物都回血', pc.hp > 1)
        gold = a.gold
        u.skills.append('pilfer')
        make_ready(u)
        u.mp = 99
        tg = foes[0]
        g.battle_cmd(a, {'u': 'p', 'a': 'skill', 's': 'pilfer', 'tg': tg.id}, clock[0])
        check('順手牽羊:偷到 敵人等級 ×3 金幣', a.gold == gold + tg.lv * 3 and bfx_of(g, 'steal'), (gold, a.gold, tg.lv))
        make_ready(u)
        g.battle_cmd(a, {'u': 'p', 'a': 'skill', 's': 'pilfer', 'tg': tg.id}, clock[0])
        check('同一隻敵人只能偷一次', a.gold == gold + tg.lv * 3)
    finally:
        server.random.random = orig
    g.leave_battle(b, a, clock[0])
    g.leave_battle(b, c, clock[0])


def test_evolve(g):
    print('\n[進化]')
    p = login(g, 'E_evo', 'knight')
    p.x, p.y = 47.5, 50.5
    pt = mkpet('poring', 11, bond=30.0)
    p.pets = [pt]
    p.ws.chats.clear()
    g.evolve(p, 0)
    check('等級不夠不能進化', pt['sp'] == 'poring' and any('Lv.12' in c for c in p.ws.chats))
    pt['exp'] = gd.exp_need(11)
    g.give_pet_exp(p, pt, 0)
    p.ws.chats.clear()
    g.evolve(p, 0)
    check('親密度不夠不能進化', pt['sp'] == 'poring' and any('親密度要 40' in c for c in p.ws.chats))
    pt['bond'] = 39.0
    p.ws.chats.clear()
    g.add_item(p, 'berry')
    pt['food'] = 50.0
    g.feed(p, 0, 'berry', clock[0])
    check('條件剛達成時通知「快要進化了」', any('快要進化' in c for c in p.ws.chats))
    p.ws.chats.clear()
    g.feed(p, 0, 'berry', clock[0])
    check('只通知一次', not any('快要進化' in c for c in p.ws.chats))
    st0, n0 = list(pt['st']), pt['n']
    pt['hp'] = 1
    g.fx.clear()
    g.evolve(p, 0)
    check('進化成中階', pt['sp'] == 'poring2' and pt['lv'] == 12)
    check('沒改過名:換成新名字', n0 == '噗噗' and pt['n'] == '彈彈噗')
    check('能力加上種族初始能力的差額', pt['st'] == [a + n - o for a, o, n in zip(st0, SP['poring']['base'], SP['poring2']['base'])])
    check('HP 補滿', pt['hp'] == gd.derive(pt['lv'], pt['st'])['mhp'])
    check('技能升階、學會專屬技能', server.skills_of(pt) == ['strike', 'heal2', 'quake2', 'jellyeat'])
    check('進化演出 (附近玩家看得到)', fx_of(g, 'evolve') and fx_of(g, 'evolve')[-1]['sp'] == 'poring2')
    pts = pt['pts']
    pt['exp'] = gd.exp_need(12)
    g.give_pet_exp(p, pt, 0)
    check('中階每升一級多 1 點', pt['pts'] == pts + 5)
    check('中階的賣價比較高', server.pet_price(pt) == server.pet_price(dict(pt, sp='poring')) + EVOLVE['price'][0])
    # 高階:改過名就保留名字、全伺服器公告
    pt['n'], pt['lv'], pt['bond'] = '小噗', 24, 70.0
    p.ws.chats.clear()
    g.evolve(p, 0)
    check('進化成高階,改過的名字保留', pt['sp'] == 'poring3' and pt['n'] == '小噗')
    check('高階全伺服器公告', any('傳說中' in c for c in p.ws.chats))
    p.ws.chats.clear()
    g.evolve(p, 0)
    check('最終型態不能再進化', pt['sp'] == 'poring3' and any('最終型態' in c for c in p.ws.chats))
    # 戰鬥中不能進化
    w = mkpet('wolf', 12, bond=50.0)
    p.pets.append(w)
    b = controlled_battle(g, p)
    g.evolve(p, 1)
    check('戰鬥中不能進化', w['sp'] == 'wolf')
    g.leave_battle(b, p, clock[0])
    # 舊存檔補值
    old = server.new_pet('fox', 5, 3)
    for k in ('inh', 'par', 'gen'):
        old.pop(k)
    server.fix_pet(old)
    check('舊存檔補值:沒有遺傳、第 1 代', old['inh'] is None and old['par'] is None and old['gen'] == 1)
    v = server.pet_view(dict(w))
    check('寵物資料帶有階段與進化條件', v['stage'] == 0 and v['evo'] == 'wolf2' and v['evo_lv'] == 12 and v['evo_bond'] == 40)


def test_breed(g):
    print('\n[發情與配對]')
    p = login(g, 'B_breed', 'hunter')
    p.x, p.y = HATCHER
    p.gold = 5000
    w, f = mkpet('wolf2', 14, q=7), mkpet('fox', 10, q=10)
    w['inh'] = 'sleep'
    p.pets = [w, f, mkpet('poring', 9)]
    check('發情:快樂 80、親密 60、沒有肚子餓', server.is_estrus(w))
    check('肚子餓就不會發情', not server.is_estrus(dict(w, food=20.0)))
    check('快樂值不夠不會發情', not server.is_estrus(dict(w, joy=79.0)))
    info = g.breed_info(p, 0, 2)
    check('Lv.10 以下不能配', not info['ok'] and any('Lv.10' in x for x in info['why']))
    f['joy'] = 50.0
    info = g.breed_info(p, 0, 1)
    check('沒發情不能配,而且說清楚差在哪裡', not info['ok'] and any('還沒發情:快樂值 50 / 80' in x for x in info['why']), info['why'])
    f['joy'] = 90.0
    info = g.breed_info(p, 0, 1)
    check('兩隻都符合:可以配', info['ok'], info['why'])
    check('小寵種族:野狼、月狐,外加混種銀月狼', [o['sp'] for o in info['opts']] == ['wolf', 'fox', 'silverwolf'])
    opt = {o['sp']: o['inh'] for o in info['opts']}
    check('遺傳候選:雙親的技能線 + 雙親的遺傳技能,扣掉小寵自己的、不含專屬技能',
          opt['wolf'] == ['sleep', 'iceball', 'icicle'] and opt['fox'] == ['double', 'gale', 'bite']
          and not any('howl' in v for v in opt.values()), opt)
    check('天生素質下限 = 雙親平均 (四捨五入)、費用 = 100 + 10 × 平均等級', info['q0'] == 9 and info['cost'] == 220,
          (info['q0'], info['cost']))
    p.x, p.y = 47.5, 50.5
    g.breed(p, 0, 1, 'wolf', 'iceball')
    check('不在婆婆旁邊不能配', not p.eggs)
    p.x, p.y = HATCHER
    g.breed(p, 0, 1, 'wolf', 'holy')
    check('不在候選裡的技能不能選', not p.eggs)
    g.breed(p, 0, 1, 'griffin', None)
    check('不在選項裡的種族不能選', not p.eggs)
    gold = p.gold
    g.fx.clear()
    g.breed(p, 0, 1, 'wolf', 'iceball')
    e = p.eggs[0] if p.eggs else {}
    check('配對成功:扣金幣、雙親快樂 −40', p.gold == gold - 220 and w['joy'] == 50 and f['joy'] == 50)
    check('得到配對蛋 (種族、素質下限、遺傳技能、雙親、第 2 代)',
          e.get('sp') == 'wolf' and e.get('q0') == 9 and e.get('inh') == 'iceball' and e.get('gen') == 2
          and [x['n'] for x in e.get('par', [])] == [w['n'], f['n']])
    check('雙親快樂值降下來,不再發情 (自然冷卻)', not server.is_estrus(w))
    check('配對的愛心演出', fx_of(g, 'pact') and fx_of(g, 'pact')[-1]['a'] == 'breed')
    m = p.ws.last('bred')
    check('通知客戶端配對成功 (配對視窗顯示結果)', m and m['sp'] == 'wolf' and m['inh'] == 'iceball' and m['q0'] == 9)
    # 混種、不遺傳技能
    w['joy'] = f['joy'] = 90.0
    g.breed(p, 0, 1, 'silverwolf', None)
    check('可以選混種、可以不選遺傳技能', len(p.eggs) == 2 and p.eggs[1]['sp'] == 'silverwolf' and p.eggs[1]['inh'] is None)
    check('配對蛋送給客戶端', p.eggs_dirty)
    w['joy'] = f['joy'] = 90.0
    g.breed(p, 0, 1, 'fox', 'double')
    w['joy'] = f['joy'] = 90.0
    info = g.breed_info(p, 0, 1)
    check('婆婆最多保管 3 顆配對蛋', len(p.eggs) == 3 and not info['ok'] and any('3 顆' in x for x in info['why']))
    # 孵配對蛋:孵得最差 = 下限,孵得最好 = 12 點
    p.pets = [w, f]
    g.hatch_start(p, None, clock[0], 0)
    h = p.hatch
    check('從婆婆那裡拿配對蛋來孵', h and h['bred'] and h['sp'] == 'wolf' and len(p.eggs) == 2)
    run(g, gd.HATCH_TIME - 0.2)
    h['sum'], h['n'] = 0.0, 10 ** 7
    run(g, 0.5)
    baby = p.pets[-1]
    check('孵得很差:天生素質 = 下限', baby['q'] == 9 and baby['sp'] == 'wolf', baby['q'])
    check('配對小寵的起始值:飽食 70、快樂 80、親密 40', (round(baby['food']), round(baby['joy']), baby['bond']) == (70, 80, 40),
          (baby['food'], baby['joy'], baby['bond']))
    check('小寵有遺傳技能、雙親、代數', baby['inh'] == 'iceball' and server.skills_of(baby) == ['double', 'iceball']
          and baby['gen'] == 2 and len(baby['par']) == 2)
    g.hatch_start(p, None, clock[0], 0)
    h = p.hatch
    run(g, gd.HATCH_TIME - 0.2)
    h['sum'], h['n'] = 10.0 ** 7, 10 ** 7
    run(g, 0.5)
    hy = p.pets[-1]
    check('孵得很好:天生素質 12 點', hy['q'] == 12, hy['q'])
    check('混種寵物孵出來了', hy['sp'] == 'silverwolf' and hy['n'] == '銀月狼' and server.skills_of(hy) == ['bite'])
    # 孵到一半離線:配對蛋還給婆婆
    p.pets = p.pets[:2]
    g.hatch_start(p, None, clock[0], 0)
    check('剩下 0 顆在婆婆那裡', not p.eggs)
    g.logout(p)
    rec = g.accounts['B_breed']
    check('孵到一半離線:配對蛋回到婆婆那裡,而且有存檔', len(rec['eggs']) == 1 and rec['eggs'][0]['sp'] == 'fox')
    p = g.login(FakeWS(), {'name': 'B_breed', 'pass': 'x'})
    check('重新登入:配對蛋還在', len(p.eggs) == 1 and p.eggs[0]['inh'] == 'double')
    check('遺傳技能與血統也有存檔', p.pets[0]['inh'] == 'sleep')
    # 婆婆的對話
    p.x, p.y = HATCHER
    g.npc_action(p, 5, 'breed', {})
    check('婆婆的「寵物配對」打開配對視窗', p.ws.last('breedui') is not None)
    g.npc_action(p, 5, 'breedhint', {})
    m = p.ws.last('dlg')
    check('「配對有什麼訣竅?」有混種的提示', m and '狼和狐狸' in m['text'])
    g.breed_preview(p, 0, 1)
    m = p.ws.last('bprev')
    check('配對預覽送給客戶端', m and m['a'] == 0 and 'opts' in m)


def main():
    test_data()
    g = server.Game()
    test_skills(g)
    test_evolve(g)
    test_breed(g)
    passed = sum(r for _, r in T.results)
    print('\n%d/%d 通過' % (passed, len(T.results)))
    sys.exit(0 if passed == len(T.results) else 1)


if __name__ == '__main__':
    main()
