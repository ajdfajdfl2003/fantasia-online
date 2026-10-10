# 遊戲圖片

- `pets/<種族>.png`:寵物主圖,例如 `poring.png`、`imp.png`(炎龍是 `dragon.png`)
- `pets/<種族>_attack.png`、`_hurt.png`、`_sleep.png`:可有可無的動作圖
- `npcs/<NPC 類別>.png`:NPC,例如 `hatcher.png`、`keeper.png`

有圖就用圖,沒圖就用程式繪圖。圖片規格、繪圖 prompt 與流程見 `docs/art/美術規格.md`;
用去背工具 `http://localhost:8000/tools/sprite-tool.html` 處理後按「存進遊戲」,就會自動放到這裡。
