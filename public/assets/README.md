# 遊戲圖片(成品)

這裡的圖是**去背工具產生的成品**,不要手動把 AI 原圖放進來。
原圖請放在專案的 `art-src/`(用中文名字,例如 `噗噗.png`),流程見 `docs/art/美術規格.md`。
成品一律是 WebP(品質 90),檔名規則見 `docs/phase-4/spec.md` 第 3 節。

- `pets/<代號>.webp`:寵物主圖,例如 `poring.webp`(噗噗)、`imp.webp`(小火妖)、`dragon.webp`(炎龍)
- `pets/<代號>_attack.webp`、`_hurt.webp`、`_sleep.webp`:可有可無的動作圖
- `owners/<職業>-<m|f>.webp`:主人,例如 `knight-m.webp`(男騎士);`_cast.webp` 是可有可無的施法圖
- `npcs/<代號>.webp`:NPC,例如 `hatcher.webp`、`keeper.webp`
- `items/<道具代號>.webp`:道具圖示,例如 `red_potion.webp`
- `ui/`:登入畫面主視覺 `login.webp`、`logo.webp`
- `ground/`:可重複鋪的地面材質,例如 `grass.webp`
- `deco/`:樹與裝飾,例如 `tree_plain1.webp`、`rock1.webp`

有圖就用圖,沒圖就用程式繪圖。
