# 幻想之境 Online — 開發守則

向 2000 年代 MMORPG 致敬的網頁多人遊戲,玩法以《寵物王 Online》(2003) 為主要參考:
寵物是戰鬥主角,玩家(主人)負責輔助。研究資料見 `docs/寵物王研究筆記.md`。

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

## 技術約定

- **零安裝**:伺服器只用 Python 3.8 標準函式庫,客戶端是純 HTML5 Canvas + 原生 JS,不引入任何套件。
- 這台電腦的 `python` 指令是微軟商店的空殼;真正的直譯器在 `%LOCALAPPDATA%\Programs\Python\Python38\python.exe`。
  Python 3.8 沒有 `match`、沒有 `X | Y` 型別寫法。
- **伺服器為準**(server-authoritative):客戶端只送操作、只負責顯示。
- 遊戲數值(寵物、技能、職業、道具、遇敵區域)全部放在 `game_data.py`,不要寫死在邏輯裡。
- 遊戲內文字、文件、commit 訊息都用**繁體中文**。

## 檔案結構

```
server.py          伺服器:HTTP + WebSocket + 遊戲邏輯(移動、戰鬥、捕捉、孵蛋、NPC、存檔)
game_data.py       遊戲數值表
public/            客戶端(index.html、style.css、*.js)
tests/             無頭模擬測試(直接呼叫伺服器邏輯,用假時鐘快轉)
docs/roadmap.md    階段總覽
docs/phase-N/      各階段的 spec.md、plan.md、handoff.md
data/              玩家存檔(不進 git)
```

## 執行與測試

```
"%LOCALAPPDATA%\Programs\Python\Python38\python.exe" server.py      # 開伺服器 → http://localhost:8000
"%LOCALAPPDATA%\Programs\Python\Python38\python.exe" tests/<測試檔>.py
```

改完伺服器邏輯要先跑無頭測試,再開瀏覽器實際玩一輪確認畫面。
