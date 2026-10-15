# 幻想之境 Online — 開發守則

向 2000 年代 MMORPG 致敬的網頁多人遊戲,玩法以《寵物王 Online》(2003) 為主要參考:
寵物是戰鬥主角,玩家(主人)負責輔助。研究資料見 `docs/寵物王研究筆記.md`。

使用者在 **Windows 和 macOS 兩台電腦**上開發,兩台的 Claude 記憶不互通。
**兩台都要知道的規則一律寫在這份檔案**,不要只存在 Claude 的記憶裡。

## 目前進度(每次告一段落時更新)

- 第四階段(美術升級)的 `docs/phase-4/spec.md`、`plan.md` 已寫好(2026-10-13),分支 `feature/phase-4-art`。
  討論與被否決的方案在 `docs/phase-4/討論紀錄.md`。
- plan 第 1 項(WebP 管線)、第 2 項(`tests/test_phase4.py` 第一部分)已完成(2026-10-13),
  第 3 項(去背工具批次模式)、第 4 項(美術進度表)、第 5 項(主人性別與主人圖)已完成(2026-10-14),
  第 6 項(繪圖 prompt)已完成(2026-10-15):`docs/art/繪圖prompt.md` 有全部 219 張圖的 prompt,「怎麼用」是批次模式的流程。
  第 6 項同時把主人用道具、丟封印卡、換寵物改成只前傾,只有技能播完整的施法動畫(spec 第 7 節)。
  第 7 項(NPC 各自的大小)已完成(2026-10-15):`ART` 每位一個 `npc_<代號>`,都是暫定值,NPC 圖進來後調。
  第 8 項(道具圖示)已完成(2026-10-16):有道具圖就用圖,去背工具支援「道具」類型。
- 第 1 批原圖在 Windows 那台(2026-10-14):在那台照 spec 第 4.4 節看原圖、用批次模式存進遊戲(plan 第 14 項),
  處理速度和去背效果記回 plan 第 3 項。
- **下次開工**:把 `docs/phase-4/下次開工prompt.md` 裡的 prompt 貼給 Claude。
  在 Windows 那台:先做上面第 1 批的 plan 第 14 項,再請使用者畫男騎士(plan 第 15 項)。程式這邊做第 9 項(技能圖示)。
- merge 回 main 前要請使用者實際看一次:第 5 項的主人動畫(女角長髮、走路搖擺、施法光芒)只看過定格畫面,
  第 6 項改的施法範圍只用程式記錄確認過(道具、封印卡只前傾,技能才發光換圖)。

## 開發流程(使用者訂的守則,每次都要遵守)

1. **git**:所有變更都進版本控制。每完成 plan 裡的一個任務就 commit 一次,訊息用繁體中文、說清楚做了什麼。
   **在 feature 分支開發**(例如 `feature/phase-2-pet-life`),不要直接 commit 到 main;
   無頭測試與瀏覽器實測都確定沒問題、使用者也確認後,才 merge 回 main(`git merge --no-ff`)。
2. **分階段**:所有功能依階段分類,總覽在 `docs/roadmap.md`。一次只做一個階段。
3. **spec → plan**:每個階段開工前,先寫 `docs/phase-N/spec.md`(要做什麼、為什麼、規則細節),
   再寫 `docs/phase-N/plan.md`(拆成可勾選的任務)。實作時照 plan 走,完成就打勾。
   做到一半發現 spec 要改,先更新 spec 再改程式。
4. **收尾與交接**:每個階段的後半段進行收尾(測試、README、說明文件),
   最後寫 `docs/phase-N/handoff.md`,內容是**下一階段的開場 prompt**,讓新的對話可以直接接手。
5. **重大設計先討論**:新系統的關鍵設計分歧(玩法方向、規則取捨)先列選項和建議,跟使用者確認後才實作。
   使用者說「我們來做 ○○」是要一起設計,不是要直接拿到成品;小修正可以直接做。

## 討論方式

- **一次只問一題**。一則訊息塞好幾題,使用者會覺得太多。
  用選擇題(AskUserQuestion)一次問一個決定,建議的選項放第一個、標上 Recommended,每個選項寫清楚代價。
- 一題裡有好幾個小決定就拆開問(例如 2-1、2-2)。
- 使用者選了不是建議的選項時,先簡短說明打算怎麼做,再追問需要的細節。
- 討論到一半要中斷時,把已定案的結論寫進 `docs/phase-N/討論紀錄.md` 並 commit,再更新上面的「目前進度」。
- 對話、遊戲內文字、文件、commit 訊息都用**繁體中文**。

## 技術約定

- **零安裝**:伺服器只用 Python 標準函式庫,客戶端是純 HTML5 Canvas + 原生 JS,不引入任何套件。
- **語法要相容 Python 3.8**(Windows 那台是 3.8.5):不能用 `match`、`X | Y` 型別、`list[int]` 這類內建泛型註記、
  `dict | dict`、`str.removeprefix()` 等 3.9 以後才有的東西。Mac 的 `python3` 比較新,在 Mac 上測試通過不代表 3.8 能跑。
- **伺服器為準**(server-authoritative):客戶端只送操作、只負責顯示。
- 遊戲數值(寵物、技能、職業、道具、遇敵區域)全部放在 `game_data.py`,不要寫死在邏輯裡。

## 檔案結構

```
server.py          伺服器:HTTP + WebSocket + 遊戲邏輯(移動、戰鬥、捕捉、孵蛋、NPC、存檔)
game_data.py       遊戲數值表
start.bat          Windows 雙擊啟動
public/            客戶端(index.html、style.css、*.js);public/tools/ 是去背工具與美術進度表
public/assets/     遊戲用的圖片成品(進 git)
art-src/           使用者用 AI 產的原圖(不進 git,見 docs/art/美術規格.md)
tests/             無頭模擬測試(直接呼叫伺服器邏輯,用假時鐘快轉);debug_server.py 是除錯伺服器
docs/roadmap.md    階段總覽
docs/phase-N/      各階段的 spec.md、plan.md、handoff.md(討論中的階段還有 討論紀錄.md)
docs/art/          美術規格與繪圖 prompt
data/              玩家存檔(不進 git)
```

## 執行與測試

**Windows**:`python` 指令是微軟商店的空殼,真正的直譯器在 `%LOCALAPPDATA%\Programs\Python\Python38\python.exe`。
```
"%LOCALAPPDATA%\Programs\Python\Python38\python.exe" server.py            # cmd / PowerShell
"$LOCALAPPDATA/Programs/Python/Python38/python.exe" tests/test_phase3.py  # Git Bash(Claude 的 Bash 工具)
```

**macOS**:
```
python3 server.py
python3 tests/test_phase3.py
```
Mac 上如果另外裝了 3.8(例如 `uv python install 3.8`),測試優先用 3.8 跑;沒有的話,merge 回 main 前要在 Windows 用 3.8 跑過一次無頭測試。
使用者的 Mac 已經用 uv 裝好 3.8.20(2026-10-12),指令是 `python3.8 tests/test_phase3.py`。

- 伺服器開在 http://localhost:8000。
- 測試檔:`tests/test_phase1.py`(加 `--balance` 跑戰鬥平衡模擬)、`test_phase2.py`、`test_phase3.py`。
- 除錯伺服器:`tests/debug_server.py [埠號]` → http://localhost:8123,存檔在 `data/debug/`,聊天輸入 `/gm` 看指令。
- 環境變數 `FANTASIA_DATA` 可以指定存檔資料夾,測試時不會動到使用者的存檔。

改完伺服器邏輯要先跑無頭測試,再開瀏覽器實際玩一輪確認畫面。

## Git 與 GitHub

- 遠端 `origin` 是私人 repo:https://github.com/ajdfajdfl2003/fantasia-online。兩台電腦靠它同步。
- 開工前先 `git pull`;commit 之後推到 origin 的同名分支,另一台電腦才拿得到。
- Mac 上的專案要放在 OneDrive 以外的資料夾。OneDrive 同步 `.git` 容易壞掉。
- `art-src/`、`data/` 不進 git。原圖在 Windows 那台的 OneDrive 裡,Mac 要用時從 OneDrive 複製。

## 開發環境注意事項(Claude 用)

- `.claude/launch.json` 每台電腦各自建立,不進 git。Mac 上的除錯伺服器設定範例:
  `{"name": "fantasia-debug", "runtimeExecutable": "python3", "runtimeArgs": ["-u", "tests/debug_server.py", "8123"], "port": 8123}`
- 用 `preview_start` 開的伺服器,回合結束會被關掉。要讓使用者玩的伺服器開在終端機分頁(`run_in_terminal`)。
- 內建瀏覽器窗格被隱藏時,`requestAnimationFrame` 會停。用 `setInterval` 自己推 frame、用 `render(t)` 定格某一刻;
  截圖是 800×450、畫布是 1280×720,`zoom` 不會放大,看小圖要自己疊一張放大的 canvas 再截圖(詳見 `docs/phase-3/handoff.md`)。
  定格的畫面看不出動畫速度和手感,merge 前請使用者實際看一次。
- 要改檔案的腳本含有反斜線或 JS 反引號時,不要用 Bash heredoc(會被吃掉),用 Write 工具寫成檔案再執行。
- 戰鬥平衡模擬每種情況只跑 60 場(誤差約 ±6%);比較改動前後,用同一個亂數種子、各跑 200 場。
- Safari 的 canvas 不能存 WebP:去背工具要用 Chrome / Edge / Firefox。
- **只有 Windows**:專案在 OneDrive 裡,不要用 `git worktree`(刪不掉);終端機管線會弄壞中文(cp950),
  中文字串改用瀏覽器或寫成檔案確認。
