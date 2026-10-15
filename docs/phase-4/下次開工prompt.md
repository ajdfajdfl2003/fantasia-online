# 下次開工的 prompt

開新對話時,把下面整段貼給 Claude。每次收工時覆蓋這份(2026-10-16 寫,接在 plan 第 8 項之後)。
跟 `handoff.md` 不同:`handoff.md` 是第五階段的開場 prompt,第四階段收尾時才寫(plan 第 27 項)。

```
照下面做。

工作目錄:/Users/ajdfajdfl/Documents/Project/fantasia-online(feature/phase-4-art)。在 Windows 那台就用那台的專案資料夾、同一個分支。

背景:幻想之境 Online 第四階段(美術升級)plan 第 1~8 項已完成並推上 origin。上一輪做的是第 6~8 項,細節看 git log 346d404..94fbcb7:
- 第 6 項:docs/art/gen_prompts.py 產生的 docs/art/繪圖prompt.md 有全部 219 張圖的 prompt(寵物、主人 10、NPC 6、道具 16、登入主視覺與 Logo、地面材質 6、樹與裝飾 9),「怎麼用」是批次模式的流程;docs/art/美術規格.md 改成 WebP、新的類別與檔名表
- 第 6 項同時跟我確認了:Logo 圖裡只畫中文;主人髮色每個職業一種、男女同色;登入主視覺是男騎士加女牧師;主人用道具、丟封印卡、換寵物只前傾,只有用技能才發光、換施法圖(spec 第 7、10 節,討論紀錄第 2、5 題)
- 第 7 項:game_data.py 的 ART 改成每位 NPC 一個 npc_<代號>,都是還沒有圖時估的暫定值
- 第 8 項:有道具圖(public/assets/items/<代號>.webp)就用圖,背包與戰鬥道具欄 32px,商店與說明框 48px,沒有圖的維持程式繪圖;去背工具加「道具」類型(64×64、置中)

開工前:
- git status 要乾淨,git fetch 後 feature/phase-4-art 不能落後遠端;不符合就停下來告訴我。
- 讀 CLAUDE.md(目前進度那段)、docs/phase-4/spec.md、docs/phase-4/plan.md(第 9 項以後)。
- 跑 open-todos 的 list,看同專案留下的項目;做完清單上的項目就標 done。

直接做的事:
- 如果這次在 Windows 上、我也說第 1 批原圖(野外與 BOSS 主圖 10 張)放進 art-src/ 了:照 spec 第 4.4 節逐張看原圖(被裁到、朝左、灰白格子背景、一張多隻、有字),有問題列出檔名和原因;沒問題再用去背工具的批次模式存進遊戲(plan 第 14 項)。處理速度和去背效果記回 plan 第 3 項(2026-10-14 在 Mac 用 3 張 1024×1024 的假原圖量,共約 1.1 秒;真的 AI 原圖還沒跑過)。
- 程式這邊做 plan 第 9 項(技能圖示:屬性色底加程式畫的符號,中階銀框、高階金框,每個技能用哪個符號寫在 game_data.py 的技能資料裡)。寫進 game_data.py 前,先把「每個技能配哪個符號」列成一張表給我看。
- 每做完 plan 的一項,照 CLAUDE.md:plan 打勾、寫結果,commit(繁體中文訊息)並推到 origin 的同名分支,再更新 CLAUDE.md 的「目前進度」。

要我決定的(一次問一題,附你的建議):
- spec 沒寫清楚的設計分歧,先列選項問我。
- 伺服器啟動時印的「區網朋友」網址,在 Mac 上會印成 127.0.0.1(用主機名稱查不到區網 IP),要不要順手修。

注意:
- Mac 的測試一律用 python3.8;Windows 用 CLAUDE.md 寫的 Python38 完整路徑。四支測試現在是 88/88、106/106、75/75、48/48。
- 瀏覽器實測需要存圖時,另外寫一個伺服器腳本,把 server.PUBLIC、server.ASSETS、server.ART_SRC 換到暫存資料夾再開,不要寫進專案的 public/assets/ 和 art-src/。
- NPC 頭上的驚嘆號高度還是寫死的(game.js 的 drawLabels),村長的圖比較高,驚嘆號會蓋在頭頂的噗噗上;留給 plan 第 16 項 NPC 圖進來時一起改。
- 男騎士(plan 第 15 項)我還沒畫。在 Mac 上畫的話,參考圖改上傳 public/assets/pets/poring.webp(Mac 沒有 art-src/噗噗.png)。
- merge 回 main 前要請我實際看一次主人動畫(女角長髮、走路搖擺、用技能的施法光芒、用道具只前傾),目前只看過定格畫面和程式記錄。真的 Safari 開去背工具留到 plan 第 25 項。
```
