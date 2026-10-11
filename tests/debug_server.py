# -*- coding: utf-8 -*-
"""
實測用的除錯伺服器:跟 server.py 一樣,多了 /gm 聊天指令,可以直接把寵物調到想看的狀態
(肚子餓、鬧脾氣、護主、離家出走……),不用真的等好幾個小時。

- 存檔放在 data/debug/(不會動到正式存檔 data/players.json),可用環境變數 FANTASIA_DATA 指定別的資料夾
- 預設開在 8123 埠:http://localhost:8123

用法:python tests/debug_server.py [埠號]
進遊戲後在聊天框輸入 /gm 看指令列表。
"""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('FANTASIA_DATA', os.path.join(ROOT, 'data', 'debug'))
sys.path.insert(0, ROOT)
import server  # noqa: E402
from server import CARE, ITEMS, PET_MAX, SKILL_TIERS, SPECIES, Game, derive, new_pet, time  # noqa: E402

HELP = ('/gm 指令(出戰寵物):food / joy / bond / sync 數值、php N(寵物 HP N%)、hp N(主人 HP N%)、'
        'enc [+N](立刻遇敵,敵人等級 +N)、sulk [秒](幾秒後離家出走)、miss(想你了)、'
        'away(下次登入算離線兩天)、pet 種族代號 [等級](新增一隻並出戰)、lv N(出戰寵物等級)、q N(天生素質)、inh 技能代號(遺傳技能)、'
        'give 道具代號 [數量]、gold N')

_chat, _wild_unit, _logout = Game.chat, Game.wild_unit, Game.logout


def gm(g, p, args):
    now = time.time()
    b = g.battles.get(p.battle)
    pt = p.pets[p.active] if p.pets else None
    pu = b.units.get(b.pu.get(p.id)) if b else None
    ou = b.units.get(b.ou.get(p.id)) if b else None
    if not args:
        return g.sys(p, HELP)
    cmd, val = args[0].lower(), args[1] if len(args) > 1 else ''
    num = lambda d=0.0: float(val) if val.lstrip('+-').replace('.', '', 1).isdigit() else d  # noqa: E731
    if cmd in ('food', 'joy', 'bond', 'sync') and pt:
        pt[cmd] = float(max(0, min(100, num())))
        if cmd == 'sync' and pu:
            pu.sync = pt['sync']
        p.pets_dirty = True
        return g.sys(p, '%s 的 %s = %g' % (pt['n'], cmd, pt[cmd]))
    if cmd == 'php' and pt:
        mhp = pu.mhp if pu else derive(pt['lv'], pt['st'])['mhp']
        hp = max(1, int(mhp * num(100) / 100))
        pt['hp'] = hp
        if pu and not pu.alive:   # 倒下了:用復活的方式救回來
            g.revive(b, pu, num(100) / 100)
        elif pu:
            pu.hp = hp
        p.pets_dirty = True
        return g.sys(p, '%s HP = %d' % (pt['n'], hp))
    if cmd == 'hp':
        hp = max(1, int(p.mhp * num(100) / 100))
        p.hp = hp
        if ou:
            ou.hp = max(1, int(ou.mhp * num(100) / 100))
        return g.sys(p, '主人 HP = %d' % (ou.hp if ou else hp))
    if cmd == 'enc':
        if p.battle or p.alive_pet() is None:
            return g.sys(p, '戰鬥中或沒有能出戰的寵物,不能遇敵。')
        g.gm_lv = int(num())
        try:
            g.start_encounter(p, now)
        finally:
            g.gm_lv = 0
        return
    if cmd == 'sulk' and pt:
        pt['food'] = pt['joy'] = 0.0
        p.sulk[pt['uid']] = CARE['sulk_leave'] - max(1.0, num(8))
        p.pets_dirty = True
        return g.sys(p, '%s 的飽食度、快樂值歸零,%g 秒後離家出走。' % (pt['n'], max(1.0, num(8))))
    if cmd == 'miss' and pt:
        g.sys(p, '%s 一看到你就撲了過來,看起來好想你!' % pt['n'])
        return g.add_fx('pact', p.x, p.y, id=p.id, a='miss', r='ok', act=1, sp=pt['sp'])
    if cmd == 'away':
        p.gm_away = True
        return g.sys(p, '下次登入時算成離線兩天。')
    if cmd == 'lv' and pt and not p.battle:
        lv = int(max(1, min(99, num(pt['lv']))))
        pt['pts'] += max(0, lv - pt['lv']) * SPECIES[pt['sp']]['grow']
        pt['lv'], pt['exp'] = lv, 0
        d = derive(lv, pt['st'])
        pt['hp'], pt['mp'] = d['mhp'], d['mmp']
        g.check_evo_ready(p, pt)
        p.pets_dirty = True
        return g.sys(p, '%s Lv.%d' % (pt['n'], lv))
    if cmd == 'inh' and pt:
        pt['inh'] = val if val in SKILL_TIERS else None
        p.pets_dirty = True
        return g.sys(p, '%s 遺傳技能 = %s' % (pt['n'], pt['inh']))
    if cmd == 'q' and pt:
        pt['q'] = int(max(0, min(12, num(pt['q']))))
        p.pets_dirty = True
        return g.sys(p, '%s 天生素質 = %d' % (pt['n'], pt['q']))
    if cmd == 'pet' and val in SPECIES:
        if len(p.pets) >= PET_MAX or p.battle:
            return g.sys(p, '身上滿了或在戰鬥中。')
        lv = int(args[2]) if len(args) > 2 and args[2].isdigit() else 5
        pt = new_pet(val, lv, 6, start='hatch')
        pt['bond'] = 70.0
        p.pets.append(pt)
        p.active = len(p.pets) - 1
        p.pets_dirty = True
        return g.sys(p, '新增 %s Lv.%d(親密度 70)並出戰。' % (pt['n'], lv))
    if cmd == 'give' and val in ITEMS:
        n = int(args[2]) if len(args) > 2 and args[2].isdigit() else 1
        for _ in range(n):
            g.add_item(p, val)
        return g.sys(p, '給了 %s ×%d' % (ITEMS[val]['name'], n))
    if cmd == 'gold':
        p.gold += int(num())
        p.inv_dirty = True
        return g.sys(p, '金幣 = %d' % p.gold)
    g.sys(p, HELP)


def chat(self, p, msg, now):
    msg = str(msg).strip()
    if msg.lower().startswith('/gm'):
        return gm(self, p, msg.split()[1:])
    return _chat(self, p, msg, now)


def wild_unit(self, sp, lv, rare=False):
    return _wild_unit(self, sp, max(1, lv + getattr(self, 'gm_lv', 0)), rare)


def logout(self, p):
    _logout(self, p)
    if getattr(p, 'gm_away', False) and p.name in self.accounts:
        self.accounts[p.name]['last'] -= 2 * 86400
        self.save()


Game.chat, Game.wild_unit, Game.logout = chat, wild_unit, logout

if __name__ == '__main__':
    server.PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
    print('[除錯伺服器] 存檔:%s  聊天輸入 /gm 看指令' % os.environ['FANTASIA_DATA'])
    try:
        asyncio.run(server.main())
    except KeyboardInterrupt:
        print('伺服器已關閉,資料已存檔。')
