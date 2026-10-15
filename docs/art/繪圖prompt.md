# 繪圖 prompt 集(ChatGPT 直接複製貼上)

每一段都是完整的 prompt,不用拼湊。規格見 `美術規格.md` 與 `docs/phase-4/spec.md`。

> 這份由 `docs/art/gen_prompts.py` 產生。要改 prompt 請改那支程式,再執行
> `python3.8 docs/art/gen_prompts.py docs/art/繪圖prompt.md`(Windows 用 Python38 的完整路徑,見 `CLAUDE.md`)。

## 怎麼用

1. **產圖**:照下面的「產圖順序」找到要畫的圖,把 prompt 貼到 ChatGPT。每個類別的開頭寫了要不要開新對話、要上傳哪張參考圖。
2. **存原圖**:下載後照箭頭後面的檔名存到 `art-src/`。一批畫完再一起處理,不用畫一張存一張。
3. **請 Claude 先看一遍**:跟 Claude 說「圖放好了」。Claude 會照 spec 第 4.4 節逐張看原圖:角色被裁到(尾巴、耳朵、翅膀出框)、
   身體朝左、灰白格子背景、一張圖裡有多隻、有文字或浮水印。有問題會列出檔名和原因,重畫或在工具裡處理(朝左就勾水平翻轉)。
4. **批次存進遊戲**:開伺服器,用 Chrome、Edge 或 Firefox(Safari 不能存 WebP)打開 <http://localhost:8000/tools/sprite-tool.html>,
   按上方的「批次」。工具會列出還沒處理的原圖,一次去背排成縮圖。看過縮圖後按「全部存進遊戲」。
   標紅的那張會跳過並寫原因;要調容許值、筆刷、翻轉就點縮圖進單張模式,修好按「存進遊戲」。
5. **看還缺哪些**:打開 <http://localhost:8000/tools/art-status.html>(美術進度表)。重新整理遊戲頁面就會看到新圖。
6. 不滿意就直接用中文跟 GPT 說要改哪裡。常見的:
   - 表情不夠兇 →「表情要更生氣,眉毛壓低成 V 字,不要笑」
   - 顏色或造型跑掉 →「顏色和造型要跟第一張完全一樣,只改姿勢和表情」
   - 角色畫太小 →「角色要跟第一張一樣大,最長邊約佔畫面 70%」
7. GPT 偶爾會把灰白格子「畫」進圖裡(看起來透明其實不是),批次模式會把這張標紅。遇到時把 `Background:` 那一行換成
   `Background: plain solid white background.`(白色系的用 `plain solid bright green background`),去背工具會處理。

> 去背工具現在支援寵物、主人、NPC、道具四類。登入主視覺與 Logo(plan 第 10 項)、地面材質與樹與裝飾(第 13 項)還沒支援:
> 原圖可以先放進 `art-src/`,批次模式會標紅寫「去背工具還沒支援」,等那一項做好再存。美術進度表照樣會算成「有原圖還沒處理」。

## 產圖順序(spec 第 2 節)

1. **第 1 批:野外與 BOSS 主圖 10 張**:綠史萊姆、哥布林、野狼、骷髏兵、月狐、彩虹鴿、吸血蝙蝠、獅鷲獸、幼龍、炎龍
2. **主人 10 張**:先畫男騎士,當人物的畫風標準圖;定案後再畫其他 9 張
3. **NPC 6 張**:要上傳男騎士和招牌寵物的成品圖,所以排在第 1 批和男騎士之後
4. **第 2 批:進化線主圖 28 張**:一條進化線開一個對話
5. **第 3 批:初階 13 種與炎龍的動作圖**(必要;噗噗、小火妖的 6 張已完成,還要 36 張)
6. 中階、高階的動作圖可有可無,有空再補,沒有的用程式動畫

道具、Logo、地面材質、樹與裝飾不依賴其他圖,隨時可以穿插。登入主視覺要等男騎士、女牧師、野狼、彩虹鴿都畫好。

## 每段 prompt 在講什麼

- **Colors**:寫死配色。重畫時顏色才不會跑掉(小火妖試做時,重畫的攻擊圖火焰顏色、角的形狀都變了)。
- **大小**:主圖和動作圖都要求「最長邊約佔畫面 70%」,動作圖再要求「跟上一張一樣大」。有翅膀的寵物要求動作圖的翅膀張開程度不變(翅膀一收一放,工具自動對齊的大小就會跑掉)。
- **Pose / Expression 分開寫**:攻擊身體往右前方衝、明講「不要笑」、眉毛壓成 V 字;受傷身體往左後倒、眼睛畫成 > <;睡著是往下彎的閉眼線。遊戲裡寵物只有 34~78px,表情要誇張才看得出來。
- 動作圖明講「不要重新設計、不要加減特徵」,也不要求火焰變小、翅膀變大這種會改變大小的動作。
- 會飛的寵物(小火妖、彩虹鴿、吸血蝙蝠)在遊戲裡是浮空的,睡著也畫成在空中打瞌睡。
- **進化型態**(中階、高階):主圖要先上傳初階的圖當參考,prompt 會要求「看得出是同一系、更大更強」。動作圖的姿勢沿用初階。程式代號是初階加 2、3(例如 `poring2`),遊戲裡顯示大小是初階的 1.15 倍、1.3 倍。
- **混種**(銀月狼、暮光鳥):只能配對得到,可以把爸媽兩張圖一起上傳當參考。
- **人物**(主人、NPC):2.5 頭身,頭約佔身高 40%。遊戲裡主人只有 52px,頭約 20px,臉和髮型才看得清楚;頭像取上半身時是頭加胸口。
  女主人跟男版同配色、同帽子武器,只換女版剪裁(例如騎士穿鎧甲短裙、獵人穿短褲)加長髮。
  髮色每個職業一種、男女同色:騎士栗棕、獵人銅紅、牧師黑、法師銀紫、吟遊詩人金。
- **主人的施法圖**:只畫動作,不畫光芒、光點、魔法陣、音符,光芒由程式畫;身體也不要前傾,前傾由程式做。只有用技能時會換成施法圖。
- **NPC 的招牌寵物**:寵物一定要貼在 NPC 身上。分開畫的話,中間的背景去掉後寵物會飄在旁邊;寵物比最大一塊的 2% 還小時,還會被「清掉小碎塊」清掉。
- **白色系**(白袍、白鬍子、白色寵物):米白色、沒有外框的部分容易被當成背景去掉,prompt 再要求一次外框;GPT 沒給透明背景就改用純綠背景。
- **道具**:成品只有 64×64,遊戲裡顯示 32px,所以要求輪廓簡單、不能有字。
- **地面材質**:從正上方看、上下左右可以無縫拼接、細節小而平均,不要大石頭或小路這種一眼看得出重複的東西;不要外框,角色站在上面才顯眼。
- **樹與裝飾**:跟寵物一樣側面站著、腳底在正中央,影子由遊戲畫。

> 階段 3(繁殖與進化)定案了全部 39 個種族:11 種 × 3 階 + 2 種混種 × 3 階。階段 4 照這份全面產圖。
> 還沒有圖的種族,遊戲會用程式繪圖;進化型態沒有圖時,用初階的圖換顏色、放大。

## 目錄

- [寵物](#寵物):39 種加炎龍,主圖與動作圖
- [主人](#主人):5 職業 × 男女 10 張
- [NPC](#npc):6 張
- [道具](#道具):16 張
- [登入畫面](#登入畫面):主視覺、Logo
- [地面材質](#地面材質):6 種,先試草地
- [樹與裝飾](#樹與裝飾):9 張

---

## 寵物

1. **每隻寵物開一個新對話**。先把 `art-src/噗噗.png` 拖進對話當參考圖,再貼「主圖」。
2. 主圖滿意後,**在同一個對話**依序貼「攻擊」「受傷」「睡著」。初階 13 種與炎龍的動作圖是必要的,中階、高階的可有可無。
   對話不見了:先上傳那隻的主圖(`art-src/名字.png`)再貼動作圖。
3. 動作圖會依主圖自動對齊大小:同一批有主圖就用同一批的,沒有就用遊戲裡的;兩邊都沒有,批次模式會標紅不存。
   批次的縮圖看起來身體跟主圖不一樣大,就點縮圖進單張模式調「動作圖大小」。

---

### 噗噗

試做。主圖和三張動作圖都畫好了,這段留著以後重畫用。

**主圖(必要)** → 存成 `art-src/噗噗.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a round pink jelly blob creature with a glossy bouncy body, a small curled sprout on top, tiny round hands and feet, two small black oval eyes, a tiny happy open-mouth smile.
Colors: bubblegum pink body with lighter pink highlights and white shine spots, black eyes, dark brown outline.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: sitting still and happy, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/噗噗_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: bubblegum pink body with lighter pink highlights and white shine spots, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squashed low and springing forward toward the right in a body-slam, the sprout on top bent backward.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/噗噗_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: bubblegum pink body with lighter pink highlights and white shine spots, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squished and tilted backward toward the left, tiny hands raised to its face, the sprout drooping.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/噗噗_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: bubblegum pink body with lighter pink highlights and white shine spots, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body flattened and relaxed on the spot, the sprout drooping down.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 彈彈噗

中階(噗噗的第二階)。開新對話,先把 `art-src/噗噗.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/彈彈噗.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a bigger round jelly blob creature with a glossy bouncy body, two curled sprouts on top, small round hands and feet, determined black oval eyes and a confident smile.
Colors: lilac purple-pink body with lighter pink highlights and white shine spots, green sprouts, black eyes, dark brown outline.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: sitting still and happy, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/彈彈噗_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lilac purple-pink body with lighter pink highlights and white shine spots, green sprouts, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squashed low and springing forward toward the right in a body-slam, the sprout on top bent backward.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/彈彈噗_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lilac purple-pink body with lighter pink highlights and white shine spots, green sprouts, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squished and tilted backward toward the left, tiny hands raised to its face, the sprout drooping.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/彈彈噗_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lilac purple-pink body with lighter pink highlights and white shine spots, green sprouts, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body flattened and relaxed on the spot, the sprout drooping down.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 噗噗國王

高階(噗噗的最終型態)。開新對話,先把 `art-src/噗噗.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/噗噗國王.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a large majestic round jelly blob king with a glossy body, a small golden crown on top, a short red royal cape, tiny round hands and feet, proud black eyes and a confident smile.
Colors: warm golden orange jelly body with light yellow highlights and white shine spots, golden crown with red jewels, red cape with white trim, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: sitting still and happy, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/噗噗國王_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: warm golden orange jelly body with light yellow highlights and white shine spots, golden crown with red jewels, red cape with white trim, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squashed low and springing forward toward the right in a body-slam, the sprout on top bent backward.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/噗噗國王_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: warm golden orange jelly body with light yellow highlights and white shine spots, golden crown with red jewels, red cape with white trim, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squished and tilted backward toward the left, tiny hands raised to its face, the sprout drooping.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/噗噗國王_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: warm golden orange jelly body with light yellow highlights and white shine spots, golden crown with red jewels, red cape with white trim, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body flattened and relaxed on the spot, the sprout drooping down.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 小火妖

試做。主圖和三張動作圖都畫好了,這段留著以後重畫用。

**主圖(必要)** → 存成 `art-src/小火妖.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a small floating fire imp spirit with a round chubby body, a big mane of wild hair made of flames, a small flame tail, two small curved horns, big golden eyes, a mischievous grin with one tiny fang, little stubby arms.
Colors: red-orange body; flame hair and flame tail with pale yellow-white centers, bright yellow middle and orange to red-orange tips; dark brown horns; golden yellow eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: floating in the air, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/小火妖_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange body; flame hair and flame tail with pale yellow-white centers, bright yellow middle and orange to red-orange tips; dark brown horns; golden yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: whole body leaning forward diagonally toward the right as if charging, both little arms thrust straight forward, the flame hair and flame tail streaming backward and keeping the same size.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout showing the tiny fang.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/小火妖_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange body; flame hair and flame tail with pale yellow-white centers, bright yellow middle and orange to red-orange tips; dark brown horns; golden yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward: body tilted back toward the left, arms flung up, the flame hair blown backward but keeping the same size.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/小火妖_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange body; flame hair and flame tail with pale yellow-white centers, bright yellow middle and orange to red-orange tips; dark brown horns; golden yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: floating curled up into a ball, arms tucked in, the flame hair resting calmly around it and keeping the same size.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 火妖

中階(小火妖的第二階)。開新對話,先把 `art-src/小火妖.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/火妖.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a bigger floating fire imp with a mane of wild flames, longer curved horns, a flame tail, sharp golden eyes, a mischievous fanged grin and little clawed arms.
Colors: deep red body; flame hair and flame tail with yellow-white centers, orange middle and crimson tips; dark brown horns; golden eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: floating in the air, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/火妖_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep red body; flame hair and flame tail with yellow-white centers, orange middle and crimson tips; dark brown horns; golden eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: whole body leaning forward diagonally toward the right as if charging, both little arms thrust straight forward, the flame hair and flame tail streaming backward and keeping the same size.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout showing the tiny fang.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/火妖_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep red body; flame hair and flame tail with yellow-white centers, orange middle and crimson tips; dark brown horns; golden eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward: body tilted back toward the left, arms flung up, the flame hair blown backward but keeping the same size.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/火妖_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep red body; flame hair and flame tail with yellow-white centers, orange middle and crimson tips; dark brown horns; golden eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: floating curled up into a ball, arms tucked in, the flame hair resting calmly around it and keeping the same size.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 炎魔

高階(小火妖的最終型態)。開新對話,先把 `art-src/小火妖.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/炎魔.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a floating flame demon lord with a crown of blue flames, big curved horns, small bat-like wings, a flame tail, glowing eyes and a confident grin.
Colors: dark navy-purple body; blue flames with white centers and cyan to deep blue tips; black horns; glowing white-blue eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: floating in the air, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/炎魔_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark navy-purple body; blue flames with white centers and cyan to deep blue tips; black horns; glowing white-blue eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: whole body leaning forward diagonally toward the right as if charging, both little arms thrust straight forward, the flame hair and flame tail streaming backward and keeping the same size.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout showing the tiny fang.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/炎魔_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark navy-purple body; blue flames with white centers and cyan to deep blue tips; black horns; glowing white-blue eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward: body tilted back toward the left, arms flung up, the flame hair blown backward but keeping the same size.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/炎魔_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark navy-purple body; blue flames with white centers and cyan to deep blue tips; black horns; glowing white-blue eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: floating curled up into a ball, arms tucked in, the flame hair resting calmly around it and keeping the same size.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 綠史萊姆

**主圖(必要)** → 存成 `art-src/綠史萊姆.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a green slime creature with a translucent droopy jelly body shaped like a water drop, two cute eyes, small bubbles inside its body.
Colors: translucent lime green body with lighter green highlights and white shine, darker green bubbles inside, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: sitting still, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/綠史萊姆_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent lime green body with lighter green highlights and white shine, darker green bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body stretching forward toward the right in a lunge, the front of the body reaching out.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/綠史萊姆_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent lime green body with lighter green highlights and white shine, darker green bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body wobbling and leaning backward toward the left, droopy.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/綠史萊姆_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent lime green body with lighter green highlights and white shine, darker green bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body melted into a low relaxed puddle shape.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 大史萊姆

中階(綠史萊姆的第二階)。開新對話,先把 `art-src/綠史萊姆.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/大史萊姆.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a big slime creature with a translucent wobbly jelly body shaped like a large water drop, two cute eyes, many bubbles inside and a small swirl on top.
Colors: translucent teal body with light aqua highlights and white shine, darker teal bubbles inside, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: sitting still, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/大史萊姆_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent teal body with light aqua highlights and white shine, darker teal bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body stretching forward toward the right in a lunge, the front of the body reaching out.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/大史萊姆_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent teal body with light aqua highlights and white shine, darker teal bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body wobbling and leaning backward toward the left, droopy.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/大史萊姆_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent teal body with light aqua highlights and white shine, darker teal bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body melted into a low relaxed puddle shape.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 史萊姆王

高階(綠史萊姆的最終型態)。開新對話,先把 `art-src/綠史萊姆.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/史萊姆王.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a huge slime king with a translucent jelly body, a small golden crown floating on top, two confident eyes and glowing bubbles inside.
Colors: translucent violet-blue body with light lavender highlights and white shine, glowing pale blue bubbles, golden crown, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: sitting still, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/史萊姆王_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent violet-blue body with light lavender highlights and white shine, glowing pale blue bubbles, golden crown, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body stretching forward toward the right in a lunge, the front of the body reaching out.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/史萊姆王_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent violet-blue body with light lavender highlights and white shine, glowing pale blue bubbles, golden crown, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body wobbling and leaning backward toward the left, droopy.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/史萊姆王_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent violet-blue body with light lavender highlights and white shine, glowing pale blue bubbles, golden crown, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body melted into a low relaxed puddle shape.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 哥布林

**主圖(必要)** → 存成 `art-src/哥布林.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a small goblin with big pointy ears, yellow eyes, a cheeky grin, a brown leather tunic, holding a wooden club.
Colors: olive green skin, yellow eyes, brown leather tunic, light brown wooden club.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing ready, holding the club, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/哥布林_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, brown leather tunic, light brown wooden club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and swinging the wooden club down from over its head.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/哥布林_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, brown leather tunic, light brown wooden club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stumbling backward toward the left, one hand holding its head, the club lowered.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/哥布林_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, brown leather tunic, light brown wooden club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: sitting on the ground with legs stretched out, hugging the club, head tilted to one side.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth slightly open with a little drool.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 哥布林戰士

中階(哥布林的第二階)。開新對話,先把 `art-src/哥布林.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/哥布林戰士.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a goblin warrior, taller and more muscular, with big pointy ears, a leather helmet, studded leather armor and a wooden club with iron spikes.
Colors: olive green skin, yellow eyes, dark brown leather helmet and armor with iron studs, wooden club with gray iron spikes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing ready, holding the club, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/哥布林戰士_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, dark brown leather helmet and armor with iron studs, wooden club with gray iron spikes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and swinging the wooden club down from over its head.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/哥布林戰士_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, dark brown leather helmet and armor with iron studs, wooden club with gray iron spikes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stumbling backward toward the left, one hand holding its head, the club lowered.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/哥布林戰士_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, dark brown leather helmet and armor with iron studs, wooden club with gray iron spikes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: sitting on the ground with legs stretched out, hugging the club, head tilted to one side.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth slightly open with a little drool.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 哥布林酋長

高階(哥布林的最終型態)。開新對話,先把 `art-src/哥布林.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/哥布林酋長.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a goblin chieftain with big pointy ears, a feathered tribal headdress, a fur cloak, war paint stripes on its cheeks and a big bone-and-stone war club.
Colors: olive green skin, yellow eyes, red and white headdress feathers, brown fur cloak, red war paint, ivory bone club.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing ready, holding the club, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/哥布林酋長_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, red and white headdress feathers, brown fur cloak, red war paint, ivory bone club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and swinging the wooden club down from over its head.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/哥布林酋長_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, red and white headdress feathers, brown fur cloak, red war paint, ivory bone club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stumbling backward toward the left, one hand holding its head, the club lowered.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/哥布林酋長_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, red and white headdress feathers, brown fur cloak, red war paint, ivory bone club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: sitting on the ground with legs stretched out, hugging the club, head tilted to one side.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth slightly open with a little drool.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 野狼

**主圖(必要)** → 存成 `art-src/野狼.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a wolf cub with fluffy fur, red eyes, small fangs, alert pointy ears, fierce but cute.
Colors: blue-gray fur with a light gray belly and muzzle, darker gray ear tips, red eyes, white fangs.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/野狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: blue-gray fur with a light gray belly and muzzle, darker gray ear tips, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/野狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: blue-gray fur with a light gray belly and muzzle, darker gray ear tips, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/野狼_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: blue-gray fur with a light gray belly and muzzle, darker gray ear tips, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up lying down with its tail wrapped around its nose.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 疾風狼

中階(野狼的第二階)。開新對話,先把 `art-src/野狼.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/疾風狼.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a young wind wolf, sleek and fast-looking, with longer legs, fur swept back like wind, sharp ears and a bushy tail.
Colors: sage green-gray fur with a pale gray belly, darker green streaks like wind, red eyes, white fangs.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/疾風狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: sage green-gray fur with a pale gray belly, darker green streaks like wind, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/疾風狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: sage green-gray fur with a pale gray belly, darker green streaks like wind, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/疾風狼_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: sage green-gray fur with a pale gray belly, darker green streaks like wind, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up lying down with its tail wrapped around its nose.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 狼王

高階(野狼的最終型態)。開新對話,先把 `art-src/野狼.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/狼王.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a majestic wolf king, large and powerful, with a thick mane of fur around its neck, a small scar over one eye, sharp fangs and a proud stance.
Colors: jet black fur with dark gray highlights, silver mane tips, glowing red eyes, white fangs.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/狼王_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: jet black fur with dark gray highlights, silver mane tips, glowing red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/狼王_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: jet black fur with dark gray highlights, silver mane tips, glowing red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/狼王_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: jet black fur with dark gray highlights, silver mane tips, glowing red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up lying down with its tail wrapped around its nose.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 骷髏兵

白色系:如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。

**主圖(必要)** → 存成 `art-src/骷髏兵.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a cute chibi skeleton warrior with a round skull and glowing eye sockets, holding a rusty short sword and a small wooden shield.
Colors: ivory white bones, glowing red eye sockets, rusty brown sword, brown wooden shield.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing ready with sword and shield, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/骷髏兵_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, rusty brown sword, brown wooden shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and slashing with the rusty sword raised high, shield held in front.
Expression: angry and fierce: the glowing red eye sockets narrowed into angry slanted slits forming a V, jaw wide open in a war cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/骷髏兵_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, rusty brown sword, brown wooden shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left, bones knocked slightly askew, skull tilted, one arm flailing.
Expression: in shock: the eye glows shrunk to tiny dots, jaw hanging wide open.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/骷髏兵_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, rusty brown sword, brown wooden shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: sitting slumped on the ground, the sword resting across its lap, skull drooping forward.
Expression: asleep: the eye glows dimmed to tiny faint dots, jaw slightly open, relaxed.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 骷髏騎士

中階(骷髏兵的第二階)。開新對話,先把 `art-src/骷髏兵.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/骷髏騎士.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a skeleton knight wearing a dented steel helmet and a breastplate, holding a longsword and a round shield.
Colors: ivory white bones, glowing red eye sockets, bluish steel helmet and breastplate, silver longsword, blue round shield.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing ready with sword and shield, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/骷髏騎士_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, bluish steel helmet and breastplate, silver longsword, blue round shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and slashing with the rusty sword raised high, shield held in front.
Expression: angry and fierce: the glowing red eye sockets narrowed into angry slanted slits forming a V, jaw wide open in a war cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/骷髏騎士_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, bluish steel helmet and breastplate, silver longsword, blue round shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left, bones knocked slightly askew, skull tilted, one arm flailing.
Expression: in shock: the eye glows shrunk to tiny dots, jaw hanging wide open.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/骷髏騎士_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, bluish steel helmet and breastplate, silver longsword, blue round shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: sitting slumped on the ground, the sword resting across its lap, skull drooping forward.
Expression: asleep: the eye glows dimmed to tiny faint dots, jaw slightly open, relaxed.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 骷髏將軍

高階(骷髏兵的最終型態)。開新對話,先把 `art-src/骷髏兵.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/骷髏將軍.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a skeleton general wearing an ornate golden helmet with a red plume, golden armor and a tattered red cape, holding a big curved greatsword.
Colors: ivory white bones, glowing red eye sockets, golden helmet and armor, red plume and cape, silver greatsword.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing ready with sword and shield, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/骷髏將軍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, golden helmet and armor, red plume and cape, silver greatsword. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and slashing with the rusty sword raised high, shield held in front.
Expression: angry and fierce: the glowing red eye sockets narrowed into angry slanted slits forming a V, jaw wide open in a war cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/骷髏將軍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, golden helmet and armor, red plume and cape, silver greatsword. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left, bones knocked slightly askew, skull tilted, one arm flailing.
Expression: in shock: the eye glows shrunk to tiny dots, jaw hanging wide open.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/骷髏將軍_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, golden helmet and armor, red plume and cape, silver greatsword. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: sitting slumped on the ground, the sword resting across its lap, skull drooping forward.
Expression: asleep: the eye glows dimmed to tiny faint dots, jaw slightly open, relaxed.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 彩虹鴿

白色系:如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。遊戲裡牠是飛在空中的,所以睡著也畫成在空中打瞌睡。動作圖大小:翅膀的張開程度會影響工具的自動對齊,存進遊戲前在工具預覽跟主圖比一下,必要時調「動作圖大小」。

**主圖(必要)** → 存成 `art-src/彩虹鴿.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a dove with a round fluffy body, a fan of rainbow colored tail feathers, an orange beak, flapping wings.
Colors: white body with pale gray wing shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings flapping, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/彩虹鴿_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white body with pale gray wing shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open in a battle cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/彩虹鴿_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white body with pale gray wing shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/彩虹鴿_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white body with pale gray wing shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while hovering in the air (it is a flying pet), head drooping onto its chest, wings spread in a slow glide with the same spread as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 虹光鴿

中階(彩虹鴿的第二階)。開新對話,先把 `art-src/彩虹鴿.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/虹光鴿.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a radiant dove, larger, with longer elegant wings, a small feather crest and a long fan of shimmering rainbow tail feathers.
Colors: cream white body with warm golden shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings flapping, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/虹光鴿_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white body with warm golden shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open in a battle cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/虹光鴿_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white body with warm golden shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/虹光鴿_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white body with warm golden shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while hovering in the air (it is a flying pet), head drooping onto its chest, wings spread in a slow glide with the same spread as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 天虹鳥

高階(彩虹鴿的最終型態)。開新對話,先把 `art-src/彩虹鴿.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/天虹鳥.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a celestial rainbow bird, majestic, with large wings, a long flowing tail of rainbow feathers, a golden feather crest and a small halo of light above its head.
Colors: golden yellow body with white highlights, rainbow tail feathers, golden crest, pale yellow halo, orange beak, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings flapping, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/天虹鳥_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: golden yellow body with white highlights, rainbow tail feathers, golden crest, pale yellow halo, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open in a battle cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/天虹鳥_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: golden yellow body with white highlights, rainbow tail feathers, golden crest, pale yellow halo, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/天虹鳥_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: golden yellow body with white highlights, rainbow tail feathers, golden crest, pale yellow halo, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while hovering in the air (it is a flying pet), head drooping onto its chest, wings spread in a slow glide with the same spread as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 月狐

白色系:如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。

**主圖(必要)** → 存成 `art-src/月狐.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a moonlight fox with a huge fluffy tail, bright eyes, a small crescent moon mark on its forehead.
Colors: white fur with pale light-blue shading, bright blue eyes, pink inner ears, pale yellow crescent moon mark.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, tail held high, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/月狐_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with pale light-blue shading, bright blue eyes, pink inner ears, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: pouncing forward toward the right with front paws raised, tail swept back.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth open showing small fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/月狐_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with pale light-blue shading, bright blue eyes, pink inner ears, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/月狐_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with pale light-blue shading, bright blue eyes, pink inner ears, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up with its huge fluffy tail wrapped around its body like a blanket.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 雪月狐

中階(月狐的第二階)。開新對話,先把 `art-src/月狐.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/雪月狐.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a snow moon fox, larger, with two fluffy tails, frosty fur tufts and a brighter crescent moon mark on its forehead.
Colors: white fur with icy blue shading, light blue tail tips, bright blue eyes, pink inner ears, silver crescent moon mark.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, tail held high, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/雪月狐_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with icy blue shading, light blue tail tips, bright blue eyes, pink inner ears, silver crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: pouncing forward toward the right with front paws raised, tail swept back.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth open showing small fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/雪月狐_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with icy blue shading, light blue tail tips, bright blue eyes, pink inner ears, silver crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/雪月狐_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with icy blue shading, light blue tail tips, bright blue eyes, pink inner ears, silver crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up with its huge fluffy tail wrapped around its body like a blanket.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 九尾月狐

高階(月狐的最終型態)。開新對話,先把 `art-src/月狐.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/九尾月狐.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: an elegant nine-tailed moon fox with nine flowing fluffy tails fanned behind it and a glowing full moon mark on its forehead.
Colors: cream white fur with warm golden shading, golden tail tips, golden eyes, pink inner ears, glowing golden full moon mark.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, tail held high, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/九尾月狐_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white fur with warm golden shading, golden tail tips, golden eyes, pink inner ears, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: pouncing forward toward the right with front paws raised, tail swept back.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth open showing small fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/九尾月狐_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white fur with warm golden shading, golden tail tips, golden eyes, pink inner ears, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/九尾月狐_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white fur with warm golden shading, golden tail tips, golden eyes, pink inner ears, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up with its huge fluffy tail wrapped around its body like a blanket.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 吸血蝙蝠

遊戲裡牠是飛在空中的,所以睡著也畫成在空中打瞌睡。動作圖大小:翅膀的張開程度會影響工具的自動對齊,存進遊戲前在工具預覽跟主圖比一下,必要時調「動作圖大小」。

**主圖(必要)** → 存成 `art-src/吸血蝙蝠.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a small vampire bat with big leathery wings, two tiny fangs, a round fuzzy body.
Colors: purple fuzzy body, darker purple wing membranes, red eyes, white fangs.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings spread open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/吸血蝙蝠_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: purple fuzzy body, darker purple wing membranes, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: swooping forward toward the right, wings spread with the same span as before.
Expression: angry and fierce, NOT smiling: brows slanted sharply down toward the center in a V shape, red eyes narrowed into a glare, mouth wide open with fangs bared.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/吸血蝙蝠_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: purple fuzzy body, darker purple wing membranes, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left in the air, wings bent but still spread with the same span as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a squeak, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/吸血蝙蝠_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: purple fuzzy body, darker purple wing membranes, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while floating in the air (it is a flying pet), wings drooping but still spread with the same span as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, the two fangs peeking out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 血翼蝠

中階(吸血蝙蝠的第二階)。開新對話,先把 `art-src/吸血蝙蝠.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/血翼蝠.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a blood-wing bat, larger, with jagged leathery wings, sharper fangs and tall pointy ears.
Colors: crimson red fuzzy body, dark red wing membranes, glowing yellow eyes, white fangs.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings spread open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/血翼蝠_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: crimson red fuzzy body, dark red wing membranes, glowing yellow eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: swooping forward toward the right, wings spread with the same span as before.
Expression: angry and fierce, NOT smiling: brows slanted sharply down toward the center in a V shape, red eyes narrowed into a glare, mouth wide open with fangs bared.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/血翼蝠_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: crimson red fuzzy body, dark red wing membranes, glowing yellow eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left in the air, wings bent but still spread with the same span as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a squeak, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/血翼蝠_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: crimson red fuzzy body, dark red wing membranes, glowing yellow eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while floating in the air (it is a flying pet), wings drooping but still spread with the same span as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, the two fangs peeking out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 夜王蝠

高階(吸血蝙蝠的最終型態)。開新對話,先把 `art-src/吸血蝙蝠.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/夜王蝠.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a regal night king bat with huge leathery wings, a high fur collar like a vampire cape, sharp fangs and a tiny silver crown.
Colors: very dark purple body, black wing membranes with purple edges, glowing red eyes, white fangs, silver crown.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings spread open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/夜王蝠_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: very dark purple body, black wing membranes with purple edges, glowing red eyes, white fangs, silver crown. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: swooping forward toward the right, wings spread with the same span as before.
Expression: angry and fierce, NOT smiling: brows slanted sharply down toward the center in a V shape, red eyes narrowed into a glare, mouth wide open with fangs bared.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/夜王蝠_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: very dark purple body, black wing membranes with purple edges, glowing red eyes, white fangs, silver crown. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left in the air, wings bent but still spread with the same span as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a squeak, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/夜王蝠_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: very dark purple body, black wing membranes with purple edges, glowing red eyes, white fangs, silver crown. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while floating in the air (it is a flying pet), wings drooping but still spread with the same span as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, the two fangs peeking out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 獅鷲獸

頭是白色:如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。動作圖大小:翅膀的張開程度會影響工具的自動對齊,存進遊戲前在工具預覽跟主圖比一下,必要時調「動作圖大小」。

**主圖(必要)** → 存成 `art-src/獅鷲獸.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a young griffin with an eagle head, a lion body, large feathered wings and a lion tail.
Colors: white eagle head, golden yellow beak, golden tan lion body, brown wings with lighter brown feather edges.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing proudly with wings half open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/獅鷲獸_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden yellow beak, golden tan lion body, brown wings with lighter brown feather edges. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: rearing up on its hind legs facing right, front talons striking forward, wings raised half open as before (not wider).
Expression: angry and fierce: brow feathers slanted sharply down toward the center in a V shape, eagle eyes narrowed into a glare, beak wide open screeching.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/獅鷲獸_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden yellow beak, golden tan lion body, brown wings with lighter brown feather edges. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, head pulled back, wings half open as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/獅鷲獸_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden yellow beak, golden tan lion body, brown wings with lighter brown feather edges. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lying down with its head resting on its front legs, wings resting half open on its back as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 獅鷲騎獸

中階(獅鷲獸的第二階)。開新對話,先把 `art-src/獅鷲獸.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/獅鷲騎獸.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: an armored griffin steed, larger, wearing a light saddle and a steel chest plate, with large feathered wings.
Colors: white eagle head, golden beak, sky blue lion body, blue and white wings, silver armor with a brown leather saddle.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing proudly with wings half open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/獅鷲騎獸_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden beak, sky blue lion body, blue and white wings, silver armor with a brown leather saddle. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: rearing up on its hind legs facing right, front talons striking forward, wings raised half open as before (not wider).
Expression: angry and fierce: brow feathers slanted sharply down toward the center in a V shape, eagle eyes narrowed into a glare, beak wide open screeching.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/獅鷲騎獸_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden beak, sky blue lion body, blue and white wings, silver armor with a brown leather saddle. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, head pulled back, wings half open as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/獅鷲騎獸_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden beak, sky blue lion body, blue and white wings, silver armor with a brown leather saddle. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lying down with its head resting on its front legs, wings resting half open on its back as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 皇家獅鷲

高階(獅鷲獸的最終型態)。開新對話,先把 `art-src/獅鷲獸.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/皇家獅鷲.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a royal griffin, majestic, with huge golden-feathered wings, a royal crest of feathers on its head and golden ornaments on its chest.
Colors: white eagle head with golden crest feathers, golden beak, golden-orange lion body, golden wings with white feather edges, red jewel ornaments.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing proudly with wings half open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/皇家獅鷲_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head with golden crest feathers, golden beak, golden-orange lion body, golden wings with white feather edges, red jewel ornaments. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: rearing up on its hind legs facing right, front talons striking forward, wings raised half open as before (not wider).
Expression: angry and fierce: brow feathers slanted sharply down toward the center in a V shape, eagle eyes narrowed into a glare, beak wide open screeching.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/皇家獅鷲_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head with golden crest feathers, golden beak, golden-orange lion body, golden wings with white feather edges, red jewel ornaments. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, head pulled back, wings half open as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/皇家獅鷲_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head with golden crest feathers, golden beak, golden-orange lion body, golden wings with white feather edges, red jewel ornaments. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lying down with its head resting on its front legs, wings resting half open on its back as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 幼龍

攻擊圖的火焰會讓面積變大,工具自動對齊後可能偏小,存進遊戲前在預覽跟主圖比一下,必要時調「動作圖大小」。

**主圖(必要)** → 存成 `art-src/幼龍.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a chubby baby dragon with two small horns, small bat-like wings and big curious eyes.
Colors: orange scales, cream colored belly, ivory horns, orange wings with lighter orange membranes, amber eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on its hind legs, wings slightly open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/幼龍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: orange scales, cream colored belly, ivory horns, orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: leaning forward toward the right and breathing a small puff of flame from its mouth, wings raised.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (the small flame coming from its mouth is the only effect allowed), only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/幼龍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: orange scales, cream colored belly, ivory horns, orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, tiny wings folded, tail curled.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/幼龍_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: orange scales, cream colored belly, ivory horns, orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up with its tail around its body.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, a tiny smoke puff from its nose.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (a tiny smoke puff from its nose is the only effect allowed), only this one character.
Square image, 1024x1024.
```

---

### 飛龍

中階(幼龍的第二階)。開新對話,先把 `art-src/幼龍.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/飛龍.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a young wyvern, slimmer and taller than a baby dragon, with larger wings, longer horns and a longer tail.
Colors: red-orange scales, cream belly, ivory horns, red-orange wings with lighter orange membranes, amber eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on its hind legs, wings slightly open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/飛龍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange scales, cream belly, ivory horns, red-orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: leaning forward toward the right and breathing a small puff of flame from its mouth, wings raised.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (the small flame coming from its mouth is the only effect allowed), only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/飛龍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange scales, cream belly, ivory horns, red-orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, tiny wings folded, tail curled.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/飛龍_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange scales, cream belly, ivory horns, red-orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up with its tail around its body.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, a tiny smoke puff from its nose.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (a tiny smoke puff from its nose is the only effect allowed), only this one character.
Square image, 1024x1024.
```

---

### 赤炎龍

高階(幼龍的最終型態)。開新對話,先把 `art-src/幼龍.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/赤炎龍.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a crimson flame dragon, powerful but still chibi, with big horns, a spiky back, large wings and embers glowing between its scales.
Colors: deep crimson scales, orange belly, ivory horns, dark red wings with orange membranes, glowing yellow eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on its hind legs, wings slightly open, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/赤炎龍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep crimson scales, orange belly, ivory horns, dark red wings with orange membranes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: leaning forward toward the right and breathing a small puff of flame from its mouth, wings raised.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (the small flame coming from its mouth is the only effect allowed), only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/赤炎龍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep crimson scales, orange belly, ivory horns, dark red wings with orange membranes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, tiny wings folded, tail curled.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/赤炎龍_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep crimson scales, orange belly, ivory horns, dark red wings with orange membranes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up with its tail around its body.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, a tiny smoke puff from its nose.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (a tiny smoke puff from its nose is the only effect allowed), only this one character.
Square image, 1024x1024.
```

---

### 銀月狼

混種(野狼 × 月狐,只能配對得到)。想讓牠像爸媽,可以把 art-src/野狼.png 和 art-src/月狐.png 一起上傳當參考。

**主圖(必要)** → 存成 `art-src/銀月狼.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a silver moon wolf cub, a hybrid of a wolf and a moon fox, with silver-blue fur, a fluffy fox-like tail, alert pointy ears and a small crescent moon mark on its forehead.
Colors: silver blue-gray fur with a pale blue belly and muzzle, white tail tip, bright blue eyes, white fangs, pale yellow crescent moon mark.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, tail held high, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/銀月狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: silver blue-gray fur with a pale blue belly and muzzle, white tail tip, bright blue eyes, white fangs, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/銀月狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: silver blue-gray fur with a pale blue belly and muzzle, white tail tip, bright blue eyes, white fangs, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/銀月狼_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: silver blue-gray fur with a pale blue belly and muzzle, white tail tip, bright blue eyes, white fangs, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up lying down with its fluffy tail wrapped around its nose.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 月影狼

中階(銀月狼的第二階)。開新對話,先把 `art-src/銀月狼.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/月影狼.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a moon shadow wolf, sleek, with flowing silver-violet fur, a fluffy tail and a glowing crescent moon mark.
Colors: lavender silver fur with violet shading, white tail tip, bright blue eyes, glowing pale yellow crescent moon mark.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, tail held high, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/月影狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lavender silver fur with violet shading, white tail tip, bright blue eyes, glowing pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/月影狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lavender silver fur with violet shading, white tail tip, bright blue eyes, glowing pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/月影狼_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lavender silver fur with violet shading, white tail tip, bright blue eyes, glowing pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up lying down with its fluffy tail wrapped around its nose.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 天狼

高階(銀月狼的最終型態)。開新對話,先把 `art-src/銀月狼.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/天狼.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a celestial wolf, majestic, with flowing white fur like starlight, a long fluffy tail with tiny sparkles and a glowing full moon mark.
Colors: shining white fur with pale silver shading, pale blue sparkles in the tail, bright blue eyes, glowing golden full moon mark.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, tail held high, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/天狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: shining white fur with pale silver shading, pale blue sparkles in the tail, bright blue eyes, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/天狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: shining white fur with pale silver shading, pale blue sparkles in the tail, bright blue eyes, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/天狼_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: shining white fur with pale silver shading, pale blue sparkles in the tail, bright blue eyes, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: curled up lying down with its fluffy tail wrapped around its nose.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 暮光鳥

混種(彩虹鴿 × 吸血蝙蝠,只能配對得到)。可以把 art-src/彩虹鴿.png 和 art-src/吸血蝙蝠.png 一起上傳當參考。會飛的寵物,睡著也畫成在空中打瞌睡。

**主圖(必要)** → 存成 `art-src/暮光鳥.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a twilight bird, a hybrid of a rainbow dove and a vampire bat, with a round fluffy body, feathered wings with small bat-like claws at the tips, a sunset colored tail fan and two tiny fangs.
Colors: dusky purple body with lavender shading, dark purple wings, tail feathers in orange, coral, magenta and indigo, golden beak, red eyes, white fangs.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings flapping, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/暮光鳥_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dusky purple body with lavender shading, dark purple wings, tail feathers in orange, coral, magenta and indigo, golden beak, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open showing tiny fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/暮光鳥_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dusky purple body with lavender shading, dark purple wings, tail feathers in orange, coral, magenta and indigo, golden beak, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/暮光鳥_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dusky purple body with lavender shading, dark purple wings, tail feathers in orange, coral, magenta and indigo, golden beak, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while hovering in the air (it is a flying pet), head drooping onto its chest, wings spread in a slow glide with the same spread as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 夜虹鳥

中階(暮光鳥的第二階)。開新對話,先把 `art-src/暮光鳥.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/夜虹鳥.png`
```
The attached image shows the first form of this creature line. Draw its evolved form (second stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look more grown-up and stronger.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a night rainbow bird, larger, with long wings and a long tail in night-sky colors dotted with tiny stars.
Colors: deep plum body, indigo wings, tail feathers in magenta, violet and indigo with white star dots, golden beak, red eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings flapping, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/夜虹鳥_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep plum body, indigo wings, tail feathers in magenta, violet and indigo with white star dots, golden beak, red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open showing tiny fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/夜虹鳥_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep plum body, indigo wings, tail feathers in magenta, violet and indigo with white star dots, golden beak, red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/夜虹鳥_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep plum body, indigo wings, tail feathers in magenta, violet and indigo with white star dots, golden beak, red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while hovering in the air (it is a flying pet), head drooping onto its chest, wings spread in a slow glide with the same spread as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 晨昏鳳凰

高階(暮光鳥的最終型態)。開新對話,先把 `art-src/暮光鳥.png` 上傳當參考圖,再貼主圖。

**主圖(必要)** → 存成 `art-src/晨昏鳳凰.png`
```
The attached image shows the first form of this creature line. Draw its final evolved form (third stage): keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), but make it look majestic and powerful, but still cute chibi.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a dawn and dusk phoenix, majestic, with large wings whose feathers fade from sunrise orange to night blue, a long flowing tail and a feather crest.
Colors: teal body; wings and tail fading from bright orange and gold to deep blue and purple; golden crest and beak; red eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings flapping, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可有可無)** → 存成 `art-src/晨昏鳳凰_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: teal body; wings and tail fading from bright orange and gold to deep blue and purple; golden crest and beak; red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open showing tiny fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可有可無)** → 存成 `art-src/晨昏鳳凰_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: teal body; wings and tail fading from bright orange and gold to deep blue and purple; golden crest and beak; red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可有可無)** → 存成 `art-src/晨昏鳳凰_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: teal body; wings and tail fading from bright orange and gold to deep blue and purple; golden crest and beak; red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: dozing while hovering in the air (it is a flying pet), head drooping onto its chest, wings spread in a slow glide with the same spread as before.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

---

### 炎龍(BOSS)

BOSS 不用畫得那麼可愛。攻擊、受傷、睡著三張動作圖都是必要的(spec 第 1 節)。翅膀的張開程度會影響工具的自動對齊,批次的縮圖看起來身體跟主圖不一樣大,就點縮圖進單張模式調「動作圖大小」。

**主圖(必要)** → 存成 `art-src/炎龍.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a huge fierce fire dragon with large horns, a spiky back, big wings spread and menacing glowing eyes, embers around it.
Colors: dark red scales, orange belly, ivory horns, black spikes, glowing yellow eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, wings spread wide, looking powerful, full body, side view facing right (three-quarter view), centered. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(必要)** → 存成 `art-src/炎龍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark red scales, orange belly, ivory horns, black spikes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: rearing up and breathing a big stream of fire forward toward the right.
Expression: furious: eyes glowing and narrowed, jaws wide open.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (the fire breath is the only effect allowed), only this one character.
Square image, 1024x1024.
```

**受傷(必要)** → 存成 `art-src/炎龍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark red scales, orange belly, ivory horns, black spikes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, head pulled back, wings still spread wide as before.
Expression: in pain: eyes squeezed tightly shut, jaws open in a roar of pain.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(必要)** → 存成 `art-src/炎龍_睡著.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark red scales, orange belly, ivory horns, black spikes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lying down on its belly with its head resting on its front legs, wings resting half open on its back.
Expression: sound asleep: eyes closed and drawn as gentle downward-curved lines, a tiny smoke puff from its nostrils.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (a tiny smoke puff from its nostrils is the only effect allowed), only this one character.
Square image, 1024x1024.
```

---

## 主人

1. **男騎士排第一**,當所有人物(主人、NPC)的畫風標準圖。開新對話,先把 `art-src/噗噗.png` 拖進去,線條和上色才會跟寵物一致,再貼主圖。
   男騎士定案、存進遊戲後,才畫其他 9 張。
2. 其他男主人:每位開一個新對話,先上傳 `art-src/男騎士.png`,再貼主圖。
3. 女主人:每位開一個新對話,先上傳 `art-src/男騎士.png`,再上傳同職業的男版圖(例如女獵人上傳 `art-src/男獵人.png`),再貼主圖。
   女騎士只要上傳男騎士。所以女版要等同職業的男版畫好。
4. 「施法」圖可有可無:主圖滿意後在同一個對話接著貼。不畫光芒、光點和音符,光芒由程式畫。
   只有用技能時會換成施法圖;用道具、丟封印卡、換寵物只前傾。沒有施法圖時,用技能是主圖前傾加光芒。
5. 只有男版圖、還沒有女版時,女角用程式繪圖(長髮),不會拿男版代替。

---

### 男騎士

人物畫風標準圖,排第一。開新對話,先把 `art-src/噗噗.png` 拖進去,再貼主圖。定案、存進遊戲後才畫其他主人。

**主圖(必要)** → 存成 `art-src/男騎士.png`
```
If I attached a reference image (a pet from the same game), match its art style exactly (outline thickness, shading, colors), but draw the human character described below. This character will be the style reference for all other human characters of the game.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young male knight wearing an open-faced silver helmet topped with a red plume, a blue tunic over light silver armor (shoulder guards and a chest plate), brown trousers and dark brown boots, holding a silver sword and a round silver shield with a red emblem; short chestnut brown hair showing under the helmet.
Colors: royal blue tunic, shiny silver helmet, armor and shield, red plume and red shield emblem, golden sword hilt, brown trousers, dark brown boots, chestnut brown hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing confidently, the sword held down at the side, the shield on the other arm, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/男騎士_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: royal blue tunic, shiny silver helmet, armor and shield, red plume and red shield emblem, golden sword hilt, brown trousers, dark brown boots, chestnut brown hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: raising the sword straight up above the head with one arm as if rallying allies, the shield held in front. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: focused and determined, eyebrows raised, mouth open as if calling out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 女騎士

開新對話,先上傳 `art-src/男騎士.png`,再貼主圖。

**主圖(必要)** → 存成 `art-src/女騎士.png`
```
The attached image is the male knight from the same game. Draw the female version of this knight: match the art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), keep the same outfit colors, the same helmet and the same weapons, only change the clothing cut to a female version and give her long hair.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young female knight wearing the same open-faced silver helmet topped with a red plume, long chestnut brown hair flowing out from under the helmet down her back with one lock framing her face, a blue tunic top over the same light silver armor (shoulder guards and a chest plate), a short armored skirt of silver plates over a blue skirt, dark brown knee-high boots, holding the same silver sword and the same round silver shield with a red emblem.
Colors: royal blue tunic and skirt, shiny silver helmet, armor, armored skirt and shield, red plume and red shield emblem, golden sword hilt, dark brown boots, chestnut brown hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing confidently, the sword held down at the side, the shield on the other arm, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/女騎士_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: royal blue tunic and skirt, shiny silver helmet, armor, armored skirt and shield, red plume and red shield emblem, golden sword hilt, dark brown boots, chestnut brown hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: raising the sword straight up above the head with one arm as if rallying allies, the shield held in front. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: focused and determined, eyebrows raised, mouth open as if calling out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 男獵人

開新對話,先上傳 `art-src/男騎士.png`,再貼主圖。

**主圖(必要)** → 存成 `art-src/男獵人.png`
```
The attached image is the male knight from the same game. Match its art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), but draw the new character described below.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young male hunter wearing a dark green cap with a white feather that has a red tip, a green hunting jacket with a brown leather belt, brown trousers and brown leather boots, holding a wooden longbow; short copper red hair.
Colors: leaf green jacket, dark green cap, white feather with a red tip, brown belt, trousers and boots, light brown wooden bow, copper red hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing relaxed, holding the bow at the side in one hand, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/男獵人_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: leaf green jacket, dark green cap, white feather with a red tip, brown belt, trousers and boots, light brown wooden bow, copper red hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: holding the bow up high in one hand and pointing forward toward the right with the other hand as if giving a command. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: focused and determined, eyebrows raised, mouth open as if calling out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 女獵人

開新對話,依序上傳 `art-src/男騎士.png`、`art-src/男獵人.png`,再貼主圖。

**主圖(必要)** → 存成 `art-src/女獵人.png`
```
I attached two images from the same game: first the male knight, then the male hunter. Match their art style exactly (2.5 heads tall proportions, outline thickness, shading, face style). Draw the female version of the hunter: keep the same outfit colors, the same hat and the same weapon as the male hunter, only change the clothing cut to a female version and give her long hair.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young female hunter wearing the same dark green cap with a white feather that has a red tip, long copper red hair flowing down her back with one lock framing her face, the same green hunting jacket with a brown leather belt, short brown shorts, brown leather knee-high boots, holding the same wooden longbow.
Colors: leaf green jacket, dark green cap, white feather with a red tip, brown belt, shorts and boots, light brown wooden bow, copper red hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing relaxed, holding the bow at the side in one hand, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/女獵人_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: leaf green jacket, dark green cap, white feather with a red tip, brown belt, shorts and boots, light brown wooden bow, copper red hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: holding the bow up high in one hand and pointing forward toward the right with the other hand as if giving a command. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: focused and determined, eyebrows raised, mouth open as if calling out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 男牧師

開新對話,先上傳 `art-src/男騎士.png`,再貼主圖。

白袍:沒給透明背景就改用純綠背景(把 `Background:` 那一行換成 `Background: plain solid bright green background.`)。2026-10-14 用假圖實測,米白色、沒有外框的身體會被當成背景去掉。

**主圖(必要)** → 存成 `art-src/男牧師.png`
```
The attached image is the male knight from the same game. Match its art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), but draw the new character described below.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young male priest wearing a tall white priest hat with a golden band and a small golden cross, a long white robe with a golden cross on the chest and golden trim at the hem and sleeves, holding a holy staff (a cream white staff topped with a golden cross); short black hair.
Colors: white robe and hat with light warm gray shading, golden cross, band and trim, cream white staff with a golden cross, black hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
The white robe and hat need the same thick dark brown outline as everything else.
Pose: standing calmly, holding the holy staff upright beside the body, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/男牧師_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: white robe and hat with light warm gray shading, golden cross, band and trim, cream white staff with a golden cross, black hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: raising the holy staff high above the head with both hands as if calling down a blessing. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: focused and determined, eyebrows raised, mouth open as if calling out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 女牧師

開新對話,依序上傳 `art-src/男騎士.png`、`art-src/男牧師.png`,再貼主圖。

白袍:沒給透明背景就改用純綠背景(把 `Background:` 那一行換成 `Background: plain solid bright green background.`)。2026-10-14 用假圖實測,米白色、沒有外框的身體會被當成背景去掉。

**主圖(必要)** → 存成 `art-src/女牧師.png`
```
I attached two images from the same game: first the male knight, then the male priest. Match their art style exactly (2.5 heads tall proportions, outline thickness, shading, face style). Draw the female version of the priest: keep the same outfit colors, the same hat and the same weapon as the male priest, only change the clothing cut to a female version and give her long hair.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young female priest wearing the same tall white priest hat with a golden band and a small golden cross, long black hair flowing down her back with one lock framing her face, a white robe dress with a fitted waist tied by a golden sash and a flared skirt, the same golden cross on the chest and golden trim, holding the same holy staff.
Colors: white robe dress and hat with light warm gray shading, golden cross, band, sash and trim, cream white staff with a golden cross, black hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
The white robe and hat need the same thick dark brown outline as everything else.
Pose: standing calmly, holding the holy staff upright beside the body, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/女牧師_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: white robe dress and hat with light warm gray shading, golden cross, band, sash and trim, cream white staff with a golden cross, black hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: raising the holy staff high above the head with both hands as if calling down a blessing. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: focused and determined, eyebrows raised, mouth open as if calling out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 男法師

開新對話,先上傳 `art-src/男騎士.png`,再貼主圖。

**主圖(必要)** → 存成 `art-src/男法師.png`
```
The attached image is the male knight from the same game. Match its art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), but draw the new character described below.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young male mage wearing a tall dark purple pointed wizard hat with a golden band, a long purple robe with golden trim, holding a wooden staff topped with a round light blue crystal; short silver-lavender hair.
Colors: purple robe, dark purple hat, golden band and trim, brown wooden staff, light blue crystal, silver-lavender hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing confidently, holding the crystal staff upright beside the body, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/男法師_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: purple robe, dark purple hat, golden band and trim, brown wooden staff, light blue crystal, silver-lavender hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: holding the crystal staff out in front toward the right with both hands, the crystal pointing forward. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: focused and determined, eyebrows raised, mouth open as if calling out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 女法師

開新對話,依序上傳 `art-src/男騎士.png`、`art-src/男法師.png`,再貼主圖。

**主圖(必要)** → 存成 `art-src/女法師.png`
```
I attached two images from the same game: first the male knight, then the male mage. Match their art style exactly (2.5 heads tall proportions, outline thickness, shading, face style). Draw the female version of the mage: keep the same outfit colors, the same hat and the same weapon as the male mage, only change the clothing cut to a female version and give her long hair.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young female mage wearing the same tall dark purple pointed wizard hat with a golden band, long silver-lavender hair flowing down her back with one lock framing her face, a purple robe dress with a fitted waist and a flared skirt to just below the knees, golden trim, dark brown short boots, holding the same wooden staff topped with a round light blue crystal.
Colors: purple robe dress, dark purple hat, golden band and trim, dark brown boots, brown wooden staff, light blue crystal, silver-lavender hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing confidently, holding the crystal staff upright beside the body, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/女法師_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: purple robe dress, dark purple hat, golden band and trim, dark brown boots, brown wooden staff, light blue crystal, silver-lavender hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: holding the crystal staff out in front toward the right with both hands, the crystal pointing forward. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: focused and determined, eyebrows raised, mouth open as if calling out.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 男吟遊詩人

開新對話,先上傳 `art-src/男騎士.png`,再貼主圖。

**主圖(必要)** → 存成 `art-src/男吟遊詩人.png`
```
The attached image is the male knight from the same game. Match its art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), but draw the new character described below.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young male bard wearing a dark blue cap with a long yellow feather, a red tunic with a golden sash across the chest, dark indigo trousers and brown boots, holding a wooden lute; short golden blonde hair.
Colors: red tunic, golden yellow sash, dark blue cap, yellow feather, dark indigo trousers, brown boots, warm brown wooden lute, golden blonde hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing cheerfully, holding the lute in front of the body, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/男吟遊詩人_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: red tunic, golden yellow sash, dark blue cap, yellow feather, dark indigo trousers, brown boots, warm brown wooden lute, golden blonde hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: strumming the lute energetically, head tilted back. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: singing happily, mouth wide open, eyes closed in joy.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

### 女吟遊詩人

開新對話,依序上傳 `art-src/男騎士.png`、`art-src/男吟遊詩人.png`,再貼主圖。

**主圖(必要)** → 存成 `art-src/女吟遊詩人.png`
```
I attached two images from the same game: first the male knight, then the male bard. Match their art style exactly (2.5 heads tall proportions, outline thickness, shading, face style). Draw the female version of the bard: keep the same outfit colors, the same hat and the same weapon as the male bard, only change the clothing cut to a female version and give her long hair.
Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: a player character (a pet trainer).
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a young female bard wearing the same dark blue cap with a long yellow feather, long golden blonde hair flowing down her back with one lock framing her face, a red tunic dress with a short flared skirt and the same golden sash across the chest, dark indigo leggings and brown boots, holding the same wooden lute.
Colors: red tunic dress, golden yellow sash, dark blue cap, yellow feather, dark indigo leggings, brown boots, warm brown wooden lute, golden blonde hair, light peach skin, dark brown eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing cheerfully, holding the lute in front of the body, full body, side view facing right (three-quarter view), centered, the face clearly visible. The character's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**施法(可有可無)** → 存成 `art-src/女吟遊詩人_施法.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions (2.5 heads tall), outline thickness, art style and these exact colors: red tunic dress, golden yellow sash, dark blue cap, yellow feather, dark indigo leggings, brown boots, warm brown wooden lute, golden blonde hair, light peach skin, dark brown eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: casting a support spell: strumming the lute energetically, head tilted back. Keep the body upright, do not lean (the game tilts the sprite forward by itself).
Expression: singing happily, mouth wide open, eyes closed in joy.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself), only this one character.
Square image, 1024x1024.
```

---

## NPC

1. **每位 NPC 開一個新對話**。先上傳男騎士的成品圖 `public/assets/owners/knight-m.webp`,再上傳招牌寵物的成品圖
   (每段開頭有寫是哪一張),再貼 prompt。所以 NPC 要等男騎士和那隻寵物都存進遊戲才畫。
2. 只畫一張站姿,呼吸、轉向玩家由程式做。名字和職務不變,改成奇幻種族混搭。
3. **招牌寵物一定要貼在 NPC 身上**(坐在頭頂、趴在背包上、抱在懷裡)。寵物跟身體中間有空隙的話,去背後寵物會飄在旁邊,
   太小的還會被「清掉小碎塊」清掉。
   Claude 看原圖時也會檢查這一點。

---

### 村長 艾倫

依序上傳 `public/assets/owners/knight-m.webp`(男騎士)、`public/assets/pets/poring.webp`(噗噗),再貼 prompt。

白色系:沒給透明背景就改用純綠背景(把 `Background:` 那一行換成 `Background: plain solid bright green background.`)。2026-10-14 用假圖實測,米白色、沒有外框的身體會被當成背景去掉。

**站姿(必要)** → 存成 `art-src/艾倫.png`
```
I attached two reference images from the same game: first the male knight (a human character), then the pet poring (a pink jelly blob). Match the knight's art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), and draw the pet exactly like its reference (same design and colors), small, as a companion.
Create a game sprite of a cute chibi NPC (a non-player character) for a 2000s Taiwanese MMORPG pet game.
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a short and stout old dwarf, the village elder: a big white beard braided into two braids, bushy white eyebrows, rosy cheeks, a green shirt under a brown leather vest, brown trousers and boots, leaning on an oak walking stick; a small poring (the pet from the second reference image) sits on top of his head.
Colors: green shirt, brown leather vest, brown trousers and boots, white beard, hair and eyebrows with light gray shading, oak brown walking stick, light peach skin with rosy cheeks; the pet: bubblegum pink body with lighter pink highlights and white shine spots, black eyes, dark brown outline.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
The pet must touch and overlap the character's body with no gap between them, so the character and the pet form one connected shape.
Pose: standing, full body, side view facing right (three-quarter view), centered, the face clearly visible. The widest or tallest side of the whole sprite (the character and the pet together) fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this character and its pet.
Square image, 1024x1024.
```

---

### 道具商人 莉莉

依序上傳 `public/assets/owners/knight-m.webp`(男騎士)、`public/assets/pets/slime.webp`(綠史萊姆),再貼 prompt。

**站姿(必要)** → 存成 `art-src/莉莉.png`
```
I attached two reference images from the same game: first the male knight (a human character), then the pet green slime. Match the knight's art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), and draw the pet exactly like its reference (same design and colors), small, as a companion.
Create a game sprite of a cute chibi NPC (a non-player character) for a 2000s Taiwanese MMORPG pet game.
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a cheerful young cat-eared girl, the item merchant: short orange hair, orange cat ears and a cat tail, a green merchant vest over a cream shirt, a big backpack on her back hung with bottles and jars, holding a red potion in one hand; a green slime (the pet from the second reference image) lies on top of the backpack.
Colors: orange hair, ears and tail, green vest, cream shirt, brown leather backpack, colorful glass bottles and jars, red potion, light peach skin; the pet: translucent lime green body with lighter green highlights and white shine, darker green bubbles inside, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
The pet must touch and overlap the character's body with no gap between them, so the character and the pet form one connected shape.
Pose: standing, full body, side view facing right (three-quarter view), centered, the face clearly visible. The widest or tallest side of the whole sprite (the character and the pet together) fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this character and its pet.
Square image, 1024x1024.
```

---

### 修女 瑪莉

依序上傳 `public/assets/owners/knight-m.webp`(男騎士)、`public/assets/pets/dove.webp`(彩虹鴿),再貼 prompt。

白色系:沒給透明背景就改用純綠背景(把 `Background:` 那一行換成 `Background: plain solid bright green background.`)。2026-10-14 用假圖實測,米白色、沒有外框的身體會被當成背景去掉。

**站姿(必要)** → 存成 `art-src/瑪莉.png`
```
I attached two reference images from the same game: first the male knight (a human character), then the pet rainbow dove. Match the knight's art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), and draw the pet exactly like its reference (same design and colors), small, as a companion.
Create a game sprite of a cute chibi NPC (a non-player character) for a 2000s Taiwanese MMORPG pet game.
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a gentle young human nun: long golden blonde hair, a white and blue nun habit with a veil, holding a holy book with both hands; a rainbow dove (the pet from the second reference image) perches on her shoulder.
Colors: white habit with blue panels, blue veil with white trim, golden blonde hair, brown holy book with golden corners, light peach skin; the pet: white body with pale gray wing shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
The white habit needs the same thick dark brown outline as everything else.
The pet must touch and overlap the character's body with no gap between them, so the character and the pet form one connected shape.
Pose: standing, full body, side view facing right (three-quarter view), centered, the face clearly visible. The widest or tallest side of the whole sprite (the character and the pet together) fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this character and its pet.
Square image, 1024x1024.
```

---

### 傳送師 奧茲

依序上傳 `public/assets/owners/knight-m.webp`(男騎士)、`public/assets/pets/fox.webp`(月狐),再貼 prompt。

白色系:沒給透明背景就改用純綠背景(把 `Background:` 那一行換成 `Background: plain solid bright green background.`)。2026-10-14 用假圖實測,米白色、沒有外框的身體會被當成背景去掉。

**站姿(必要)** → 存成 `art-src/奧茲.png`
```
I attached two reference images from the same game: first the male knight (a human character), then the pet moon fox. Match the knight's art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), and draw the pet exactly like its reference (same design and colors), small, as a companion.
Create a game sprite of a cute chibi NPC (a non-player character) for a 2000s Taiwanese MMORPG pet game.
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: an elegant elf, the teleporter: long silver-white hair, long pointed elf ears, a deep blue robe and a pointed hat decorated with small stars like a starry night sky, holding a staff topped with a shining blue crystal (a painted highlight only, no glow around it); a moon fox (the pet from the second reference image) is draped around the shoulders like a scarf.
Colors: deep navy blue robe and hat with small pale yellow stars, silver-white hair, brown wooden staff, bright blue crystal, light peach skin; the pet: white fur with pale light-blue shading, bright blue eyes, pink inner ears, pale yellow crescent moon mark.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
The pet must touch and overlap the character's body with no gap between them, so the character and the pet form one connected shape.
Pose: standing, full body, side view facing right (three-quarter view), centered, the face clearly visible. The widest or tallest side of the whole sprite (the character and the pet together) fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this character and its pet.
Square image, 1024x1024.
```

---

### 孵化屋 葛莉絲婆婆

依序上傳 `public/assets/owners/knight-m.webp`(男騎士)、`public/assets/pets/imp.webp`(小火妖),再貼 prompt。

白色系:沒給透明背景就改用純綠背景(把 `Background:` 那一行換成 `Background: plain solid bright green background.`)。2026-10-14 用假圖實測,米白色、沒有外框的身體會被當成背景去掉。

**站姿(必要)** → 存成 `art-src/葛莉絲婆婆.png`
```
I attached two reference images from the same game: first the male knight (a human character), then the pet fire imp. Match the knight's art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), and draw the pet exactly like its reference (same design and colors), small, as a companion.
Create a game sprite of a cute chibi NPC (a non-player character) for a 2000s Taiwanese MMORPG pet game.
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a small, kind old rabbit-eared grandma: gray-white floppy rabbit ears, gray-white hair, round glasses, a long purple robe, carrying a basket full of eggs on one arm; a fire imp (the pet from the second reference image) sits inside the basket hugging an egg to keep it warm.
Colors: gray-white ears and hair, purple robe, round glasses with thin brown frames, light brown woven basket, cream and pastel colored eggs, light peach skin; the pet: red-orange body; flame hair and flame tail with pale yellow-white centers, bright yellow middle and orange to red-orange tips; dark brown horns; golden yellow eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
The pet must touch and overlap the character's body with no gap between them, so the character and the pet form one connected shape.
Pose: standing, full body, side view facing right (three-quarter view), centered, the face clearly visible. The widest or tallest side of the whole sprite (the character and the pet together) fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this character and its pet.
Square image, 1024x1024.
```

---

### 寵物旅館 蘿絲

依序上傳 `public/assets/owners/knight-m.webp`(男騎士)、`public/assets/pets/drake.webp`(幼龍),再貼 prompt。

**站姿(必要)** → 存成 `art-src/蘿絲.png`
```
I attached two reference images from the same game: first the male knight (a human character), then the pet baby dragon. Match the knight's art style exactly (2.5 heads tall proportions, outline thickness, shading, face style), and draw the pet exactly like its reference (same design and colors), small, as a companion.
Create a game sprite of a cute chibi NPC (a non-player character) for a 2000s Taiwanese MMORPG pet game.
Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, so keep the shapes bold and simple.
Character: a cheerful young dog-eared girl, the pet hotel keeper: reddish-brown twin tails, floppy dog ears, a pink dress with a white apron, holding a baby dragon (the pet from the second reference image) in her arms.
Colors: reddish-brown hair and dog ears, pink dress, white apron, brown shoes, light peach skin; the pet: orange scales, cream colored belly, ivory horns, orange wings with lighter orange membranes, amber eyes.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
The pet must touch and overlap the character's body with no gap between them, so the character and the pet form one connected shape.
Pose: standing, full body, side view facing right (three-quarter view), centered, the face clearly visible. The widest or tallest side of the whole sprite (the character and the pet together) fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this character and its pet.
Square image, 1024x1024.
```

---

## 道具

- 開一個新對話,先把 `art-src/噗噗.png` 拖進去當參考圖,畫風才跟寵物一樣,再一張一張貼。同一個對話接著畫,畫風比較一致。
- 成品是 64×64、置中;背包和戰鬥道具欄顯示 32px,商店與說明視窗放大到 48px。沒有圖的道具維持程式繪圖。
- 6 種蛋各長不一樣,看得出是哪種寵物的蛋。
- 去背工具的「道具」類型會把圖裁到剛好、置中存成 64×64,批次模式也認得道具的原圖。

**紅色藥水** → 存成 `art-src/紅色藥水.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a round glass potion bottle with a cork stopper, filled with bright red liquid.
Colors: bright red liquid, clear glass with a light blue tint and a white shine, light brown cork.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**藍色藥水** → 存成 `art-src/藍色藥水.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a round glass potion bottle with a cork stopper, filled with bright blue liquid.
Colors: bright blue liquid, clear glass with a light blue tint and a white shine, light brown cork.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**復活草** → 存成 `art-src/復活草.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a small bundle of a magical healing herb: a few bright green leaves on a short stem with one tiny white flower bud.
Colors: bright green leaves with lighter green veins, white flower bud with a pale yellow center.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**封印卡** → 存成 `art-src/封印卡.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a magic sealing card: a rectangular card with rounded corners, tilted slightly, with a simple golden magic circle pattern on it (only shapes, no letters or symbols that look like writing).
Colors: lavender purple card, golden border and pattern, white highlight.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**小火妖蛋** → 存成 `art-src/小火妖蛋.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a pet egg, oval and standing upright, with yellow flame-shaped patterns rising from the bottom (the egg of a little fire imp).
Colors: red-orange shell with a white shine, yellow and orange flame patterns.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

白色的蛋:沒給透明背景就改用純綠背景(把 `Background:` 那一行換成 `Background: plain solid bright green background.`)。2026-10-14 用假圖實測,米白色、沒有外框的身體會被當成背景去掉。

**彩虹鴿蛋** → 存成 `art-src/彩虹鴿蛋.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a pet egg, oval and standing upright, with soft rainbow stripes wrapping around its middle (the egg of a rainbow dove).
Colors: white shell with pale gray shading, stripes in red, yellow, green, blue and purple.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**月狐蛋** → 存成 `art-src/月狐蛋.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a pet egg, oval and standing upright, with a crescent moon mark and a few tiny stars (the egg of a moon fox).
Colors: pale icy blue shell with a white shine, pale yellow crescent moon and stars.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**吸血蝙蝠蛋** → 存成 `art-src/吸血蝙蝠蛋.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a pet egg, oval and standing upright, with a dark bat-wing pattern on its sides (the egg of a vampire bat).
Colors: dark purple shell with a lighter purple shine, black bat-wing pattern, a few small red spots.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**獅鷲獸蛋** → 存成 `art-src/獅鷲獸蛋.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a pet egg, oval and standing upright, with brown feather-shaped speckles (the egg of a griffin).
Colors: golden tan shell with a white shine, brown feather patterns.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**幼龍蛋** → 存成 `art-src/幼龍蛋.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a pet egg, oval and standing upright, covered in a scale pattern, with two tiny horn-like bumps on top (the egg of a baby dragon).
Colors: orange shell with a darker orange scale pattern and cream highlights, ivory bumps.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**鮮肉** → 存成 `art-src/鮮肉.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a fresh raw meat steak on a bone, cartoon style.
Colors: red-pink meat with light pink marbling, ivory bone.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**鮮魚** → 存成 `art-src/鮮魚.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a fresh whole fish lying on its side, cartoon style.
Colors: blue back fading to a silver-white belly, light blue fins, black eye.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**莓果** → 存成 `art-src/莓果.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a small cluster of round wild berries with two green leaves.
Colors: magenta-purple berries with white shine spots, green leaves.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**麥穗** → 存成 `art-src/麥穗.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: three golden ears of wheat tied together with a string.
Colors: golden yellow wheat, light brown string.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**木材** → 存成 `art-src/木材.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a small bundle of three firewood logs tied with a rope.
Colors: brown bark, light tan cut ends with tree rings, beige rope.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

**礦石** → 存成 `art-src/礦石.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the item described below.
Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Item: a rough chunk of rock ore with shiny crystals sticking out of it.
Colors: blue-gray rock, sparkling light blue and silver crystals.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: one single item, seen slightly from the front and above, centered, filling about 80% of the image. In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.
Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, no frame or border, no glow or sparkles, no extra objects, only this one item.
Square image, 1024x1024.
```

---

## 登入畫面

- **主視覺**:要等男騎士、女牧師、野狼、彩虹鴿都畫好。開新對話,依序上傳 `art-src/男騎士.png`、`art-src/女牧師.png`、
  `art-src/噗噗.png`、`art-src/小火妖.png`、`art-src/野狼.png`、`art-src/彩虹鴿.png`,再貼 prompt。
  成品 1536×1024,鋪滿登入畫面的背景,中間放登入框;現在的天空動畫會改成疊在上面的飄動光點。
- **Logo**:圖裡只畫「幻想之境」四個字,英文「FANTASIA ONLINE」維持網頁字,放在 Logo 圖下面。
  中文字常畫錯,每張都要逐字看「幻、想、之、境」筆畫對不對;試很多次都畫不好,就維持現在的網頁字。
- 去背工具還沒有「登入主視覺」「Logo」類型(plan 第 10 項),原圖先放進 `art-src/`。

**主視覺** → 存成 `art-src/登入畫面.png`
```
I attached six reference images from the same game, in this order: the male knight, the female priest, the pet poring (a pink jelly blob), the pet fire imp, the pet wolf cub and the pet rainbow dove. Draw all of them exactly like their references (same designs and colors) and match their art style.
Create the title screen key art for a 2000s Taiwanese MMORPG pet game, in a bright fairy-tale adventure mood.
Scene: a sunny blue sky with big fluffy white clouds over a green rolling meadow with a few flowers, a small cozy village with red roofs in the middle distance, and far away to the north a volcano with the dark silhouette of a huge fire dragon on top of it.
Foreground: the male knight on the left side and the female priest on the right side, both happy and ready for an adventure; the poring and the wolf cub near the knight, the fire imp floating near the priest, the rainbow dove flying in the sky above them.
Composition: keep the center of the image calm and open (only sky and meadow, no characters and no important details there): a login box will cover about the middle 35% of the width and most of the height. Put the characters only in the left and right thirds of the image.
Style: the characters keep the same thick dark brown outlines and cel shading as the references; the background is softer and more painterly, with lighter outlines, so the characters stand out.
No text, no logo, no letters, no user interface, no frame or border.
Landscape image, 1536x1024.
```

**Logo** → 存成 `art-src/Logo.png`
```
Create a game title logo for a 2000s Taiwanese MMORPG pet game.
Text: exactly these four Traditional Chinese characters on one line, from left to right: 幻想之境 (幻, 想, 之, 境). Draw every stroke of each character correctly. No other text: no English, no extra characters, no subtitle.
Lettering: bold brush-calligraphy style characters (like kaishu), golden with a gradient from pale cream at the top to deep orange-gold at the bottom, a slight 3D bevel and a glossy highlight, a thick dark brown outline around every character.
Decoration: none, or only a small simple ornament attached to the letters (for example a tiny star at the end of a stroke); nothing floating separately.
Background: transparent background (PNG). No shadow, no glow, no sparkles, no frame, no scene behind the text.
Landscape image, 1536x1024. The logo fills about 80% of the width, centered.
```

---

## 地面材質

- **先試草地一種**。存進遊戲看效果,好看再畫其他 5 種;不好看就退回程式繪圖,其他 5 種不用畫(spec 第 11 節)。
- 原圖 1024 會縮成 256×256,一張蓋地圖 8×8 格。工具會做無縫化(位移一半、融合接縫),也會顯示 3×3 拼起來的樣子看重複感。
- 不用參考圖,每種開新對話直接貼。水面的水波動畫還是程式畫,材質只要平靜的水面。
- 去背工具還沒有「地面材質」類型(plan 第 13 項),原圖先放進 `art-src/`。

**草地(先試這張)** → 存成 `art-src/地面_草地.png`
```
Create a seamless tileable ground texture for the top-down 2D map of a 2000s Taiwanese MMORPG pet game.
Ground: short lush meadow grass made of many tiny grass blades, with a few very small lighter and darker patches.
Colors: medium grass green (about #4c9637), lighter green blade tips (about #67b64c), slightly darker green shading (about #43872f).
View: seen straight from above (top-down), flat, no perspective, no horizon, no sky.
Seamless: the texture must tile without visible seams: the left edge continues into the right edge, and the top edge continues into the bottom edge.
Detail: the whole image covers 8 x 8 squares of the game map, so keep the details small and spread evenly over the whole image (many small details, not a few big ones). No single large feature (no big rock, no path, no puddle) that would make the repetition obvious. No cast shadows, even lighting across the whole image, no darker corners or vignette.
Style: soft cel-shaded cartoon style that fits cute chibi game characters, but no dark outlines, and a little less saturated than the characters so they stand out on top of it.
No text, no characters, no objects other than the small ground details described above.
Square image, 1024x1024.
```

**森林草地(草地好看才畫)** → 存成 `art-src/地面_森林草地.png`
```
Create a seamless tileable ground texture for the top-down 2D map of a 2000s Taiwanese MMORPG pet game.
Ground: shady forest floor grass made of many tiny dark grass blades, with a few tiny fallen leaves and small moss patches.
Colors: dark forest green (about #3a6630), lighter green blade tips (about #4f8443), darker shading (about #2e5226).
View: seen straight from above (top-down), flat, no perspective, no horizon, no sky.
Seamless: the texture must tile without visible seams: the left edge continues into the right edge, and the top edge continues into the bottom edge.
Detail: the whole image covers 8 x 8 squares of the game map, so keep the details small and spread evenly over the whole image (many small details, not a few big ones). No single large feature (no big rock, no path, no puddle) that would make the repetition obvious. No cast shadows, even lighting across the whole image, no darker corners or vignette.
Style: soft cel-shaded cartoon style that fits cute chibi game characters, but no dark outlines, and a little less saturated than the characters so they stand out on top of it.
No text, no characters, no objects other than the small ground details described above.
Square image, 1024x1024.
```

**沙路(草地好看才畫)** → 存成 `art-src/地面_沙路.png`
```
Create a seamless tileable ground texture for the top-down 2D map of a 2000s Taiwanese MMORPG pet game.
Ground: a sandy dirt path surface: fine sand with many tiny pebbles.
Colors: warm sand beige (about #d2ad72), light tan grains (about #ddbd88), small darker brown pebbles (about #9c8058).
View: seen straight from above (top-down), flat, no perspective, no horizon, no sky.
Seamless: the texture must tile without visible seams: the left edge continues into the right edge, and the top edge continues into the bottom edge.
Detail: the whole image covers 8 x 8 squares of the game map, so keep the details small and spread evenly over the whole image (many small details, not a few big ones). No single large feature (no big rock, no path, no puddle) that would make the repetition obvious. No cast shadows, even lighting across the whole image, no darker corners or vignette.
Style: soft cel-shaded cartoon style that fits cute chibi game characters, but no dark outlines, and a little less saturated than the characters so they stand out on top of it.
No text, no characters, no objects other than the small ground details described above.
Square image, 1024x1024.
```

**村莊石板(草地好看才畫)** → 存成 `art-src/地面_村莊石板.png`
```
Create a seamless tileable ground texture for the top-down 2D map of a 2000s Taiwanese MMORPG pet game.
Ground: village pavement made of rectangular stone slabs laid in staggered rows with thin grout lines, about 16 rows of slabs across the image; the rows must line up across the edges so the pattern continues.
Colors: warm light gray stone (about #a29e93) with lighter top edges (about #b9b5aa), darker gray grout lines (about #7d796f).
View: seen straight from above (top-down), flat, no perspective, no horizon, no sky.
Seamless: the texture must tile without visible seams: the left edge continues into the right edge, and the top edge continues into the bottom edge.
Detail: the whole image covers 8 x 8 squares of the game map, so keep the details small and spread evenly over the whole image (many small details, not a few big ones). No single large feature (no big rock, no path, no puddle) that would make the repetition obvious. No cast shadows, even lighting across the whole image, no darker corners or vignette.
Style: soft cel-shaded cartoon style that fits cute chibi game characters, but no dark outlines, and a little less saturated than the characters so they stand out on top of it.
No text, no characters, no objects other than the small ground details described above.
Square image, 1024x1024.
```

**荒原焦土(草地好看才畫)** → 存成 `art-src/地面_荒原焦土.png`
```
Create a seamless tileable ground texture for the top-down 2D map of a 2000s Taiwanese MMORPG pet game.
Ground: scorched wasteland ground: dark cracked burnt earth covered with ash, with a few tiny orange-red embers.
Colors: dark brown-gray earth (about #4a3934), darker cracks (about #3b2c28), tiny orange-red embers (about #d0582a).
View: seen straight from above (top-down), flat, no perspective, no horizon, no sky.
Seamless: the texture must tile without visible seams: the left edge continues into the right edge, and the top edge continues into the bottom edge.
Detail: the whole image covers 8 x 8 squares of the game map, so keep the details small and spread evenly over the whole image (many small details, not a few big ones). No single large feature (no big rock, no path, no puddle) that would make the repetition obvious. No cast shadows, even lighting across the whole image, no darker corners or vignette.
Style: soft cel-shaded cartoon style that fits cute chibi game characters, but no dark outlines, and a little less saturated than the characters so they stand out on top of it.
No text, no characters, no objects other than the small ground details described above.
Square image, 1024x1024.
```

**水面(草地好看才畫)** → 存成 `art-src/地面_水面.png`
```
Create a seamless tileable ground texture for the top-down 2D map of a 2000s Taiwanese MMORPG pet game.
Ground: a calm lake water surface with soft gentle ripples only; keep it simple because the game animates the waves on top.
Colors: clear blue (about #2d6cc0), lighter blue ripple highlights (about #4a8ad8).
View: seen straight from above (top-down), flat, no perspective, no horizon, no sky.
Seamless: the texture must tile without visible seams: the left edge continues into the right edge, and the top edge continues into the bottom edge.
Detail: the whole image covers 8 x 8 squares of the game map, so keep the details small and spread evenly over the whole image (many small details, not a few big ones). No single large feature (no big rock, no path, no puddle) that would make the repetition obvious. No cast shadows, even lighting across the whole image, no darker corners or vignette.
Style: soft cel-shaded cartoon style that fits cute chibi game characters, but no dark outlines, and a little less saturated than the characters so they stand out on top of it.
No text, no characters, no objects other than the small ground details described above.
Square image, 1024x1024.
```

---

## 樹與裝飾

- 開一個新對話,先把 `art-src/噗噗.png` 拖進去當參考圖,再一張一張貼。
- 樹依區域換圖:艾爾文草原用草原樹,迷霧森林和狼嚎之丘用森林樹,亡者荒原用枯樹。岩石和草叢只是點綴,花叢畫在花地上。
- 岩石、草叢、花叢要連成一塊:比最大一塊的 2% 還小的碎塊,去背時會被「清掉小碎塊」清掉。大小之後用比例對照頁定。
- 去背工具還沒有「樹與裝飾」類型(plan 第 13 項),原圖先放進 `art-src/`。

**草原樹1** → 存成 `art-src/草原樹1.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a round leafy meadow tree with a short thick trunk and a big fluffy rounded crown made of a few leaf clusters.
Colors: bright green leaves with light green highlights and dark green shading, warm brown trunk.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```

**草原樹2** → 存成 `art-src/草原樹2.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a smaller young meadow tree with a slightly lopsided oval crown of lighter leaves and a thin trunk.
Colors: fresh light green leaves with yellow-green highlights and green shading, light brown trunk.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```

**森林樹1** → 存成 `art-src/森林樹1.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a tall pine tree made of three stacked triangular tiers of needles and a short trunk.
Colors: dark green needles with blue-green highlights, dark brown trunk.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```

**森林樹2** → 存成 `art-src/森林樹2.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a slim spruce tree with drooping layered branches, taller and narrower than a pine.
Colors: deep blue-green needles with lighter green tips, dark brown trunk.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```

**荒原枯樹** → 存成 `art-src/荒原枯樹.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a dead leafless tree from a burnt wasteland: a twisted trunk and bare crooked branches.
Colors: charcoal gray-brown bark with lighter gray highlights.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```

**岩石1** → 存成 `art-src/岩石1.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a medium boulder with a few cracks and a small patch of moss on top.
Colors: gray stone with light gray highlights and darker gray shading, green moss.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```

**岩石2** → 存成 `art-src/岩石2.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a small cluster of two or three rocks of different sizes, touching each other.
Colors: warm gray stone with light highlights and darker shading.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```

**草叢** → 存成 `art-src/草叢.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a low clump of tall wild grass blades growing from one spot.
Colors: grass green blades with light green tips and darker green at the base.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```

**花叢** → 存成 `art-src/花叢.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the object described below.
Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.
Object: a small low clump of wild flowers with green leaves, all growing from one spot.
Colors: red, yellow, white, pink-purple and blue flowers with yellow centers, green leaves.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), the whole object visible, centered. The object's widest or tallest side fills about 70% of the image.
Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, no extra objects, only this one object.
Square image, 1024x1024.
```
