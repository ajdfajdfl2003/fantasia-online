# 階段 2 交接(中途:還沒完成)

> 這份是第二階段做到一半、換新對話時用的。階段 2 全部完成後(plan 第 16 項),
> 這份會改寫成「第三階段的開場 prompt」。

## 目前狀態(2026-10-11)
- 分支:**`feature/phase-2-pet-life`**,還沒 merge 回 main(守則:測試 + 實測 + 使用者確認後才 merge)。
- plan 第 1~12 項完成(照顧、互動、旅館、助攻、護主、讀圖系統、去背工具)。
- 測試:`tests/test_phase2.py` 103/103、`tests/test_phase1.py` 88/88。
- 圖:噗噗四張(主圖、攻擊、受傷、睡著)和小火妖主圖已進遊戲;小火妖動作圖要用修訂後的 prompt 重畫。
- 剩下:第 13 項試做(小火妖動作圖、畫風還沒定案)、第 14 項實測(動畫還沒親眼看過)、
  第 15 項 roadmap 狀態、第 16 項第三階段交接,最後 merge。各項進度寫在 `plan.md`。

## 開發 / 測試小技巧(這次踩到的)
- **伺服器要開在使用者的終端機分頁**(`run_in_terminal`),不要用 `preview_start`:
  preview 伺服器會在回合結束時被 app 關掉。改了伺服器程式要重開,重開前先看終端機有沒有人在線上。
- 測試用另一份存檔:設環境變數 `FANTASIA_DATA=<資料夾>` 再開伺服器,就不會動到 `data/players.json`。
- Claude 的瀏覽器窗格被隱藏時 `requestAnimationFrame` 會停:畫面要手動 `render(t)` / `UI.tick(t)` / `updateFollowers(0.016)`,
  而且截圖不會更新,只能用 `ctx.getImageData` 檢查像素。動畫的視覺確認最好請使用者看。
- Bash 工具的 heredoc 會把 `\\` 吃成 `\`:要寫含反斜線的腳本,用 Write 工具寫成檔案再執行。
- 使用者的原圖在 `art-src/`(中文檔名,不進 git);成品由去背工具寫到 `public/assets/`。

---

## 繼續第二階段的開場 prompt

把下面這段貼到新的對話:

```
我們繼續《幻想之境 Online》的第二階段:寵物生活 + 圖片管線(做到一半)。

請先閱讀:
1. CLAUDE.md(開發守則,一定要照著做;注意要在 feature 分支開發)
2. docs/phase-2/handoff.md(目前狀態與開發小技巧)
3. docs/phase-2/spec.md 和 docs/phase-2/plan.md(規格與進度,第 13 項之後還沒做完)
4. docs/art/美術規格.md 和 docs/art/繪圖prompt.md(圖片流程)

目前在 feature/phase-2-pet-life 分支,還沒 merge 回 main。
接下來:
- 第 13 項:我會用修訂後的 prompt 重畫小火妖的攻擊 / 受傷 / 睡著放到 art-src/,一起用去背工具放進遊戲,
  比較 Q 版和像素化,定案畫風並寫回 spec
- 第 14 項:實測(動畫、泡泡、護主、表演等還沒親眼看過),修 bug、調數值
- 第 15、16 項:更新 roadmap 狀態,寫第三階段(繁殖與進化)的交接
- 全部確認沒問題後再 merge 回 main
```
