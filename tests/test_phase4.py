# -*- coding: utf-8 -*-
"""
階段 4 無頭測試:美術升級(WebP 圖片管線:檔名檢查、WebP 檔頭、圖片清單、快取標頭)。
沿用階段 1 的測試工具;圖片一律存到暫存資料夾,不會動到 public/assets/。

用法:python tests/test_phase4.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_phase1 as T   # noqa: E402  (載入時會把伺服器的時鐘換成假時鐘)
from test_phase1 import check  # noqa: E402

server, gd = T.server, T.gd
WEBP = b'RIFF\x10\x00\x00\x00WEBPVP8 fake-body'
PNG = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR fake-body'


# ============================================================
def test_art_names():
    print('\n[圖片檔名:spec 第 3 節的規則]')
    good = ['pets/poring.webp', 'owners/knight-f.webp', 'owners/bard-m_cast.webp', 'items/red_potion.webp',
            'ui/logo.webp', 'ground/grass.webp', 'deco/tree_dead.webp']
    check('各分類的合法檔名都接受', all(server.art_path(n) for n in good), [n for n in good if not server.art_path(n)])
    check('合法檔名對應到 assets 底下的同名檔案',
          server.art_path('owners/knight-f.webp') == os.path.join(server.ASSETS, 'owners', 'knight-f.webp'))
    up = ['../owners/knight-m.webp', 'owners/../server.webp', 'items/../../server.webp', 'ui/../../../logo.webp']
    check('含 ../ 的檔名拒絕', all(server.art_path(n) is None for n in up), [n for n in up if server.art_path(n)])
    unknown = ['pets/unicorn.webp', 'owners/thief-m.webp', 'items/gold_potion.webp', 'ui/banner.webp',
               'ground/lava.webp', 'deco/tree_palm.webp']
    check('不存在的代號拒絕', all(server.art_path(n) is None for n in unknown), [n for n in unknown if server.art_path(n)])
    png = ['owners/knight-m.png', 'items/red_potion.png', 'ui/logo.png', 'ground/grass.png', 'deco/tree_dead.png']
    check('.png 檔名拒絕', all(server.art_path(n) is None for n in png), [n for n in png if server.art_path(n)])
    owner = ['owners/knight.webp', 'owners/knight-.webp', 'owners/knight-x.webp', 'owners/knight_cast.webp']
    check('主人少了性別或性別不是 m / f 拒絕', all(server.art_path(n) is None for n in owner),
          [n for n in owner if server.art_path(n)])
    frame = ['owners/knight-m_attack.webp', 'owners/priest-f_sleep.webp', 'owners/mage-f_dance.webp']
    check('主人的動作圖不是 cast 拒絕', all(server.art_path(n) is None for n in frame),
          [n for n in frame if server.art_path(n)])
    trailing = ['owners/mage-f_.webp', 'pets/poring_.webp']
    check('檔名結尾多一個底線拒絕', all(server.art_path(n) is None for n in trailing),
          [n for n in trailing if server.art_path(n)])


def test_art_save_and_manifest():
    print('\n[圖片存檔與清單]')
    orig = server.ASSETS
    server.ASSETS = os.path.join(T.TMP, 'assets')
    try:
        target = os.path.join(server.ASSETS, 'owners', 'knight-m.webp')
        ok, msg = server.save_art('owners/knight-m.webp', PNG)
        check('PNG 檔頭冒充 WebP 拒絕、不寫檔', not ok and not os.path.exists(target), msg)
        ok, msg = server.save_art('items/red_potion.webp', PNG)
        check('道具圖用 PNG 檔頭也拒絕', not ok and not os.path.exists(os.path.join(server.ASSETS, 'items', 'red_potion.webp')), msg)

        names = ['owners/knight-f.webp', 'owners/bard-m_cast.webp', 'items/red_potion.webp', 'ui/logo.webp',
                 'ground/grass.webp', 'deco/tree_dead.webp']
        saved = [n for n in names if server.save_art(n, WEBP)[0]]
        check('新分類的 WebP 都存得進去', saved == names, sorted(set(names) - set(saved)))
        # 手動放一張舊的 PNG,清單不該列出來
        open(os.path.join(server.ASSETS, 'items', 'old_potion.png'), 'wb').write(PNG)
        m = server.asset_manifest()
        listed = sorted(f['p'] for f in m['files'])
        check('清單列出新分類底下的 .webp', listed == sorted(names), listed)
        check('清單不列 .png', not any(p.endswith('.png') for p in listed), listed)
        check('清單每張圖都帶版本號 (修改時間)', all(isinstance(f['v'], int) and f['v'] > 0 for f in m['files']), m['files'])
    finally:
        server.ASSETS = orig


def test_src_mtime():
    print('\n[原圖清單附修改時間 (批次模式判斷「原圖比成品新」)]')
    orig = server.ART_SRC
    server.ART_SRC = os.path.join(T.TMP, 'art-src')
    os.makedirs(server.ART_SRC, exist_ok=True)
    try:
        for fn, t in (('野狼.png', 1760000000), ('噗噗_攻擊.jpg', 1760000500), ('notes.txt', 1760000900)):
            path = os.path.join(server.ART_SRC, fn)
            open(path, 'wb').write(b'x')
            os.utime(path, (t, t))
        m = server.asset_manifest()
        check('清單附上每張原圖的修改時間,不列非圖片檔', m.get('srcv') == {'野狼.png': 1760000000, '噗噗_攻擊.jpg': 1760000500},
              m.get('srcv'))
    finally:
        server.ART_SRC = orig


def test_catalog():
    print('\n[要畫的圖清單 (美術進度表與去背工具共用)]')
    check('遊戲登入時讀的清單不帶完整圖片清單 (維持小檔)', 'catalog' not in server.asset_manifest())
    cat = server.asset_manifest(catalog=True).get('catalog') or []
    count = {}
    for e in cat:
        count[e['g']] = count.get(e['g'], 0) + 1
    want = {'pet': 40, 'frame': 42, 'frame_opt': 78, 'owner': 10, 'owner_opt': 10, 'npc': 6, 'item': 16,
            'ui': 2, 'ground': 6, 'deco': 9}
    check('各類別的張數跟 spec 第 1、5 節一樣', count == want, count)
    required = sum(n for g, n in want.items() if not g.endswith('_opt'))
    check('必要的圖加起來 131 張', sum(n for g, n in count.items() if not g.endswith('_opt')) == required == 131)
    check('清單裡每張圖的檔名都通過存檔檢查', cat and all(server.art_path(e['p']) for e in cat),
          [e['p'] for e in cat if not server.art_path(e['p'])])
    check('沒有重複的成品', len({e['p'] for e in cat}) == len(cat))
    by = {e['p']: e for e in cat}
    samples = {'pets/poring_attack.webp': ['噗噗_攻擊', 'poring_attack'], 'pets/dragon.webp': ['炎龍', 'dragon'],
               'owners/knight-m.webp': ['男騎士', 'knight-m'], 'owners/priest-f_cast.webp': ['女牧師_施法'],
               'npcs/elder.webp': ['村長 艾倫', '艾倫', 'elder'], 'items/red_potion.webp': ['紅色藥水', 'red_potion'],
               'ui/logo.webp': ['Logo'], 'ground/grass.webp': ['地面_草地'], 'deco/tree_dead.webp': ['荒原枯樹']}
    miss = [(p, n) for p, names in samples.items() for n in names if n not in (by.get(p) or {}).get('src', [])]
    check('原圖檔名照 spec 第 3 節 (中文名、代號都認)', not miss, miss)
    owner = {e['g'] for e in cat if e['p'].startswith('owners/') and '_cast' not in e['p']}
    check('動作圖分成必要 (初階與炎龍) 和可有可無 (中高階)',
          by['pets/wolf_hurt.webp']['g'] == 'frame' and by['pets/dragon_sleep.webp']['g'] == 'frame'
          and by['pets/wolf2_hurt.webp']['g'] == 'frame_opt' and by['owners/bard-f_cast.webp']['g'] == 'owner_opt'
          and owner == {'owner'})
    names = [n for e in cat for n in {x.lower() for x in e['src']}]   # 比對時不分大小寫 (Logo、logo 是同一張)
    dup = sorted({n for n in names if names.count(n) > 1})
    check('同一個原圖檔名不會對到兩張圖', not dup, dup)


def test_cache_control():
    print('\n[快取標頭]')
    long_cache = 'public, max-age=31536000, immutable'
    check('帶 v 的 /assets/ 圖片回長快取', server.cache_control('/assets/pets/poring.webp', 'v=1760000000') == long_cache)
    check('新分類帶 v 也回長快取', server.cache_control('/assets/owners/knight-f.webp', 'v=1760000000') == long_cache)
    check('/assets/ 沒帶 v 回 no-cache', server.cache_control('/assets/pets/poring.webp', '') == 'no-cache')
    check('/assets.json 回 no-cache', server.cache_control('/assets.json', '') == 'no-cache')
    check('/assets.json 帶 v 也回 no-cache', server.cache_control('/assets.json', 'v=1760000000') == 'no-cache')
    check('/index.html 回 no-cache', server.cache_control('/index.html', '') == 'no-cache')


def test_owner_sex():
    print('\n[主人的性別 (spec 第 7、15 節)]')
    g = server.Game()
    p = g.login(T.FakeWS(), {'name': 'X_girl', 'pass': 'x', 'cls': 'priest', 'sex': 'f'})
    check('新角色選女:登入後是女', p and p.sex == 'f')
    check('進遊戲的訊息帶性別', p.ws.last('welcome').get('sex') == 'f')
    g.logout(p)
    check('存檔有 sex 欄位', g.accounts['X_girl'].get('sex') == 'f', g.accounts['X_girl'].get('sex'))
    g2 = server.Game()   # 重新讀存檔
    p = g2.login(T.FakeWS(), {'name': 'X_girl', 'pass': 'x', 'cls': 'knight', 'sex': 'm'})
    check('重新登入還是女 (登入畫面選的性別只在建立新角色時有用)', p.sex == 'f' and p.cls == 'priest', (p.sex, p.cls))
    check('重新登入的進遊戲訊息也是女', p.ws.last('welcome').get('sex') == 'f')
    g2.logout(p)

    old = dict(g2.accounts['X_girl'])
    old.pop('sex')
    g2.accounts['X_old'] = old
    p = g2.login(T.FakeWS(), {'name': 'X_old', 'pass': 'x', 'sex': 'f'})
    check('舊存檔沒有 sex:登入是男', p and p.sex == 'm', p and p.sex)
    g2.logout(p)
    g2.accounts['X_odd'] = dict(old, sex='F')
    p = g2.login(T.FakeWS(), {'name': 'X_odd', 'pass': 'x'})
    check('存檔裡的性別不是 f:當作男', p.sex == 'm', p.sex)
    g2.logout(p)

    bad = []
    for i, sex in enumerate(('x', 'F', '', None, 1, ['f'], {'f': 1})):
        ws = T.FakeWS()
        q = g2.login(ws, {'name': 'X_bad%d' % i, 'pass': 'x', 'cls': 'mage', 'sex': sex})
        if not q or q.sex != 'm' or ws.last('err'):
            bad.append(sex)
        if q:
            g2.logout(q)
    check('建立角色時性別不合法:當作男,不回錯誤', not bad, bad)
    ws = T.FakeWS()
    q = g2.login(ws, {'name': 'X_none', 'pass': 'x', 'cls': 'mage'})
    check('登入訊息沒帶性別:當作男', q and q.sex == 'm')
    g2.logout(q)

    a = g2.login(T.FakeWS(), {'name': 'X_seeA', 'pass': 'x', 'cls': 'bard', 'sex': 'f'})
    b = g2.login(T.FakeWS(), {'name': 'X_seeB', 'pass': 'x', 'cls': 'knight'})
    b.x, b.y = a.x, a.y
    g2.send_snaps(T.clock[0])
    ents = {e['n']: e for e in b.ws.last('snap')['e']}
    check('地圖快照帶性別,別的玩家看得到', ents.get('X_seeA', {}).get('sx') == 'f' and ents.get('X_seeB', {}).get('sx') == 'm',
          {n: e.get('sx') for n, e in ents.items()})
    bt = T.controlled_battle(g2, a)
    g2.send_snaps(T.clock[0])
    units = [u for x in b.ws.last('snap')['bt'] if x['i'] == bt.id for u in x['u']]
    owner = [u for u in units if u['k'] == 'o']
    check('戰鬥單位的主人帶性別', len(owner) == 1 and owner[0].get('sx') == 'f', owner)
    check('寵物與敵人不帶性別', all('sx' not in u for u in units if u['k'] != 'o'))
    g2.logout(a)
    g2.logout(b)
    check('主人的顯示大小 52px', gd.ART.get('owner', {}).get('size') == 52, gd.ART.get('owner'))


# ============================================================
def test_npc_sizes():
    print('\n[NPC 各自的大小:spec 第 8 節]')
    codes = [n['c'] for n in server.NPCS]
    missing = [c for c in codes if not gd.ART.get('npc_' + c, {}).get('size')]
    check('每位 NPC 在 ART 都有自己的大小', not missing, missing)
    check('不再有共用的 npc 大小', 'npc' not in gd.ART)
    extra = [k for k in gd.ART if k.startswith('npc_') and k[4:] not in codes]
    check('ART 裡沒有對不上 NPC 的 npc_ 代號', not extra, extra)
    art = server.asset_manifest()['art']
    check('圖片清單帶著每位 NPC 的大小', all(art.get('npc_' + c) == gd.ART['npc_' + c] for c in codes))


def main():
    test_owner_sex()
    test_npc_sizes()
    test_art_names()
    test_art_save_and_manifest()
    test_src_mtime()
    test_catalog()
    test_cache_control()
    passed = sum(r for _, r in T.results)
    print('\n%d/%d 通過' % (passed, len(T.results)))
    sys.exit(0 if passed == len(T.results) else 1)


if __name__ == '__main__':
    main()
