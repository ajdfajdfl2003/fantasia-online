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


def test_cache_control():
    print('\n[快取標頭]')
    long_cache = 'public, max-age=31536000, immutable'
    check('帶 v 的 /assets/ 圖片回長快取', server.cache_control('/assets/pets/poring.webp', 'v=1760000000') == long_cache)
    check('新分類帶 v 也回長快取', server.cache_control('/assets/owners/knight-f.webp', 'v=1760000000') == long_cache)
    check('/assets/ 沒帶 v 回 no-cache', server.cache_control('/assets/pets/poring.webp', '') == 'no-cache')
    check('/assets.json 回 no-cache', server.cache_control('/assets.json', '') == 'no-cache')
    check('/assets.json 帶 v 也回 no-cache', server.cache_control('/assets.json', 'v=1760000000') == 'no-cache')
    check('/index.html 回 no-cache', server.cache_control('/index.html', '') == 'no-cache')


def main():
    test_art_names()
    test_art_save_and_manifest()
    test_src_mtime()
    test_cache_control()
    passed = sum(r for _, r in T.results)
    print('\n%d/%d 通過' % (passed, len(T.results)))
    sys.exit(0 if passed == len(T.results) else 1)


if __name__ == '__main__':
    main()
