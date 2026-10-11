# 繪圖 prompt 集(ChatGPT 直接複製貼上)

每一段都是完整的 prompt,不用拼湊。規格與流程見 `美術規格.md`。

> 這份由 `docs/art/gen_prompts.py` 產生。要改 prompt 請改那支程式,再執行 `python docs/art/gen_prompts.py docs/art/繪圖prompt.md`。

## 怎麼用

1. **每隻寵物開一個新對話**。想讓畫風跟噗噗一樣,先把 `art-src/噗噗.png` 拖進對話(當參考圖),再貼「主圖」。
2. 主圖滿意後,**在同一個對話**依序貼「攻擊」「受傷」「睡著」(這三張可有可無)。
   對話不見了:先上傳那隻的主圖(`art-src/名字.png`)再貼動作圖。
3. 每張下載後,照箭頭後面的檔名存到 `art-src/`,再開去背工具按「存進遊戲」。
4. 不滿意就直接用中文跟 GPT 說要改哪裡。常見的:
   - 表情不夠兇 →「表情要更生氣,眉毛壓低成 V 字,不要笑」
   - 顏色或造型跑掉 →「顏色和造型要跟第一張完全一樣,只改姿勢和表情」
   - 角色畫太小 →「角色要跟第一張一樣大,最長邊約佔畫面 70%」
5. 存動作圖時,工具會依遊戲裡的主圖自動對齊大小。預覽右邊會並排主圖,身體看起來不一樣大就調「動作圖大小」。
6. GPT 偶爾會把灰白格子「畫」進圖裡(看起來透明其實不是)。遇到時把 `Background:` 那一行換成
   `Background: plain solid white background.`(白色系的寵物用 `plain solid bright green background`),去背工具會處理。

## 每段 prompt 在講什麼
- **Colors**:寫死配色。重畫時顏色才不會跑掉(小火妖試做時,重畫的攻擊圖火焰顏色、角的形狀都變了)。
- **大小**:主圖和動作圖都要求「最長邊約佔畫面 70%」,動作圖再要求「跟上一張一樣大」。有翅膀的寵物要求動作圖的翅膀張開程度不變(翅膀一收一放,工具自動對齊的大小就會跑掉)。
- **Pose / Expression 分開寫**:攻擊身體往右前方衝、明講「不要笑」、眉毛壓成 V 字;受傷身體往左後倒、眼睛畫成 > <;睡著是往下彎的閉眼線。遊戲裡寵物只有 34~78px,表情要誇張才看得出來。
- 動作圖明講「不要重新設計、不要加減特徵」,也不要求火焰變小、翅膀變大這種會改變大小的動作。
- 會飛的寵物(小火妖、彩虹鴿、吸血蝙蝠)在遊戲裡是浮空的,睡著也畫成在空中打瞌睡。

- **進化型態**(中階、高階):主圖要先上傳初階的圖當參考,prompt 會要求「看得出是同一系、更大更強」。動作圖的姿勢沿用初階。程式代號是初階加 2、3(例如 `poring2`),遊戲裡顯示大小是初階的 1.15 倍、1.3 倍。
- **混種**(銀月狼、暮光鳥):只能配對得到,可以把爸媽兩張圖一起上傳當參考。

> 階段 3(繁殖與進化)定案了全部 39 個種族:11 種 × 3 階 + 2 種混種 × 3 階。階段 4 照這份全面產圖。
> 還沒有圖的種族,遊戲會用程式繪圖;進化型態沒有圖時,用初階的圖換顏色、放大。

---

## 噗噗

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

**攻擊(可選)** → 存成 `art-src/噗噗_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: bubblegum pink body with lighter pink highlights and white shine spots, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squashed low and springing forward toward the right in a body-slam, the sprout on top bent backward.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/噗噗_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: bubblegum pink body with lighter pink highlights and white shine spots, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squished and tilted backward toward the left, tiny hands raised to its face, the sprout drooping.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/噗噗_睡著.png`
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

## 彈彈噗

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

**攻擊(可選)** → 存成 `art-src/彈彈噗_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lilac purple-pink body with lighter pink highlights and white shine spots, green sprouts, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squashed low and springing forward toward the right in a body-slam, the sprout on top bent backward.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/彈彈噗_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lilac purple-pink body with lighter pink highlights and white shine spots, green sprouts, black eyes, dark brown outline. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squished and tilted backward toward the left, tiny hands raised to its face, the sprout drooping.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/彈彈噗_睡著.png`
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

## 噗噗國王

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

**攻擊(可選)** → 存成 `art-src/噗噗國王_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: warm golden orange jelly body with light yellow highlights and white shine spots, golden crown with red jewels, red cape with white trim, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squashed low and springing forward toward the right in a body-slam, the sprout on top bent backward.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/噗噗國王_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: warm golden orange jelly body with light yellow highlights and white shine spots, golden crown with red jewels, red cape with white trim, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body squished and tilted backward toward the left, tiny hands raised to its face, the sprout drooping.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/噗噗國王_睡著.png`
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

## 小火妖

試做。主圖、攻擊、受傷都完成了,只剩睡著。請在產主圖的那個對話接著貼;對話不見了就先上傳 art-src/小火妖.png 再貼。

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

**攻擊(可選)** → 存成 `art-src/小火妖_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange body; flame hair and flame tail with pale yellow-white centers, bright yellow middle and orange to red-orange tips; dark brown horns; golden yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: whole body leaning forward diagonally toward the right as if charging, both little arms thrust straight forward, the flame hair and flame tail streaming backward and keeping the same size.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout showing the tiny fang.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/小火妖_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange body; flame hair and flame tail with pale yellow-white centers, bright yellow middle and orange to red-orange tips; dark brown horns; golden yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward: body tilted back toward the left, arms flung up, the flame hair blown backward but keeping the same size.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/小火妖_睡著.png`
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

## 火妖

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

**攻擊(可選)** → 存成 `art-src/火妖_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep red body; flame hair and flame tail with yellow-white centers, orange middle and crimson tips; dark brown horns; golden eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: whole body leaning forward diagonally toward the right as if charging, both little arms thrust straight forward, the flame hair and flame tail streaming backward and keeping the same size.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout showing the tiny fang.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/火妖_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep red body; flame hair and flame tail with yellow-white centers, orange middle and crimson tips; dark brown horns; golden eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward: body tilted back toward the left, arms flung up, the flame hair blown backward but keeping the same size.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/火妖_睡著.png`
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

## 炎魔

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

**攻擊(可選)** → 存成 `art-src/炎魔_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark navy-purple body; blue flames with white centers and cyan to deep blue tips; black horns; glowing white-blue eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: whole body leaning forward diagonally toward the right as if charging, both little arms thrust straight forward, the flame hair and flame tail streaming backward and keeping the same size.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout showing the tiny fang.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/炎魔_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark navy-purple body; blue flames with white centers and cyan to deep blue tips; black horns; glowing white-blue eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward: body tilted back toward the left, arms flung up, the flame hair blown backward but keeping the same size.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/炎魔_睡著.png`
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

## 綠史萊姆

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

**攻擊(可選)** → 存成 `art-src/綠史萊姆_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent lime green body with lighter green highlights and white shine, darker green bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body stretching forward toward the right in a lunge, the front of the body reaching out.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/綠史萊姆_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent lime green body with lighter green highlights and white shine, darker green bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body wobbling and leaning backward toward the left, droopy.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/綠史萊姆_睡著.png`
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

## 大史萊姆

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

**攻擊(可選)** → 存成 `art-src/大史萊姆_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent teal body with light aqua highlights and white shine, darker teal bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body stretching forward toward the right in a lunge, the front of the body reaching out.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/大史萊姆_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent teal body with light aqua highlights and white shine, darker teal bubbles inside, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body wobbling and leaning backward toward the left, droopy.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/大史萊姆_睡著.png`
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

## 史萊姆王

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

**攻擊(可選)** → 存成 `art-src/史萊姆王_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent violet-blue body with light lavender highlights and white shine, glowing pale blue bubbles, golden crown, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body stretching forward toward the right in a lunge, the front of the body reaching out.
Expression: angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/史萊姆王_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: translucent violet-blue body with light lavender highlights and white shine, glowing pale blue bubbles, golden crown, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: body wobbling and leaning backward toward the left, droopy.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/史萊姆王_睡著.png`
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

## 哥布林

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

**攻擊(可選)** → 存成 `art-src/哥布林_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, brown leather tunic, light brown wooden club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and swinging the wooden club down from over its head.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/哥布林_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, brown leather tunic, light brown wooden club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stumbling backward toward the left, one hand holding its head, the club lowered.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/哥布林_睡著.png`
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

## 哥布林戰士

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

**攻擊(可選)** → 存成 `art-src/哥布林戰士_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, dark brown leather helmet and armor with iron studs, wooden club with gray iron spikes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and swinging the wooden club down from over its head.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/哥布林戰士_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, dark brown leather helmet and armor with iron studs, wooden club with gray iron spikes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stumbling backward toward the left, one hand holding its head, the club lowered.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/哥布林戰士_睡著.png`
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

## 哥布林酋長

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

**攻擊(可選)** → 存成 `art-src/哥布林酋長_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, red and white headdress feathers, brown fur cloak, red war paint, ivory bone club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and swinging the wooden club down from over its head.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/哥布林酋長_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: olive green skin, yellow eyes, red and white headdress feathers, brown fur cloak, red war paint, ivory bone club. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stumbling backward toward the left, one hand holding its head, the club lowered.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/哥布林酋長_睡著.png`
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

## 野狼

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

**攻擊(可選)** → 存成 `art-src/野狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: blue-gray fur with a light gray belly and muzzle, darker gray ear tips, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/野狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: blue-gray fur with a light gray belly and muzzle, darker gray ear tips, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/野狼_睡著.png`
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

## 疾風狼

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

**攻擊(可選)** → 存成 `art-src/疾風狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: sage green-gray fur with a pale gray belly, darker green streaks like wind, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/疾風狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: sage green-gray fur with a pale gray belly, darker green streaks like wind, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/疾風狼_睡著.png`
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

## 狼王

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

**攻擊(可選)** → 存成 `art-src/狼王_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: jet black fur with dark gray highlights, silver mane tips, glowing red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/狼王_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: jet black fur with dark gray highlights, silver mane tips, glowing red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/狼王_睡著.png`
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

## 骷髏兵

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

**攻擊(可選)** → 存成 `art-src/骷髏兵_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, rusty brown sword, brown wooden shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and slashing with the rusty sword raised high, shield held in front.
Expression: angry and fierce: the glowing red eye sockets narrowed into angry slanted slits forming a V, jaw wide open in a war cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/骷髏兵_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, rusty brown sword, brown wooden shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left, bones knocked slightly askew, skull tilted, one arm flailing.
Expression: in shock: the eye glows shrunk to tiny dots, jaw hanging wide open.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/骷髏兵_睡著.png`
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

## 骷髏騎士

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

**攻擊(可選)** → 存成 `art-src/骷髏騎士_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, bluish steel helmet and breastplate, silver longsword, blue round shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and slashing with the rusty sword raised high, shield held in front.
Expression: angry and fierce: the glowing red eye sockets narrowed into angry slanted slits forming a V, jaw wide open in a war cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/骷髏騎士_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, bluish steel helmet and breastplate, silver longsword, blue round shield. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left, bones knocked slightly askew, skull tilted, one arm flailing.
Expression: in shock: the eye glows shrunk to tiny dots, jaw hanging wide open.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/骷髏騎士_睡著.png`
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

## 骷髏將軍

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

**攻擊(可選)** → 存成 `art-src/骷髏將軍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, golden helmet and armor, red plume and cape, silver greatsword. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: stepping forward toward the right and slashing with the rusty sword raised high, shield held in front.
Expression: angry and fierce: the glowing red eye sockets narrowed into angry slanted slits forming a V, jaw wide open in a war cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/骷髏將軍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: ivory white bones, glowing red eye sockets, golden helmet and armor, red plume and cape, silver greatsword. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left, bones knocked slightly askew, skull tilted, one arm flailing.
Expression: in shock: the eye glows shrunk to tiny dots, jaw hanging wide open.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/骷髏將軍_睡著.png`
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

## 彩虹鴿

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

**攻擊(可選)** → 存成 `art-src/彩虹鴿_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white body with pale gray wing shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open in a battle cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/彩虹鴿_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white body with pale gray wing shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/彩虹鴿_睡著.png`
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

## 虹光鴿

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

**攻擊(可選)** → 存成 `art-src/虹光鴿_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white body with warm golden shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open in a battle cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/虹光鴿_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white body with warm golden shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/虹光鴿_睡著.png`
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

## 天虹鳥

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

**攻擊(可選)** → 存成 `art-src/天虹鳥_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: golden yellow body with white highlights, rainbow tail feathers, golden crest, pale yellow halo, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open in a battle cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/天虹鳥_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: golden yellow body with white highlights, rainbow tail feathers, golden crest, pale yellow halo, orange beak, black eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/天虹鳥_睡著.png`
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

## 月狐

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

**攻擊(可選)** → 存成 `art-src/月狐_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with pale light-blue shading, bright blue eyes, pink inner ears, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: pouncing forward toward the right with front paws raised, tail swept back.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth open showing small fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/月狐_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with pale light-blue shading, bright blue eyes, pink inner ears, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/月狐_睡著.png`
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

## 雪月狐

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

**攻擊(可選)** → 存成 `art-src/雪月狐_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with icy blue shading, light blue tail tips, bright blue eyes, pink inner ears, silver crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: pouncing forward toward the right with front paws raised, tail swept back.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth open showing small fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/雪月狐_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white fur with icy blue shading, light blue tail tips, bright blue eyes, pink inner ears, silver crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/雪月狐_睡著.png`
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

## 九尾月狐

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

**攻擊(可選)** → 存成 `art-src/九尾月狐_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white fur with warm golden shading, golden tail tips, golden eyes, pink inner ears, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: pouncing forward toward the right with front paws raised, tail swept back.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth open showing small fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/九尾月狐_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: cream white fur with warm golden shading, golden tail tips, golden eyes, pink inner ears, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/九尾月狐_睡著.png`
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

## 吸血蝙蝠

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

**攻擊(可選)** → 存成 `art-src/吸血蝙蝠_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: purple fuzzy body, darker purple wing membranes, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: swooping forward toward the right, wings spread with the same span as before.
Expression: angry and fierce, NOT smiling: brows slanted sharply down toward the center in a V shape, red eyes narrowed into a glare, mouth wide open with fangs bared.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/吸血蝙蝠_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: purple fuzzy body, darker purple wing membranes, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left in the air, wings bent but still spread with the same span as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a squeak, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/吸血蝙蝠_睡著.png`
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

## 血翼蝠

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

**攻擊(可選)** → 存成 `art-src/血翼蝠_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: crimson red fuzzy body, dark red wing membranes, glowing yellow eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: swooping forward toward the right, wings spread with the same span as before.
Expression: angry and fierce, NOT smiling: brows slanted sharply down toward the center in a V shape, red eyes narrowed into a glare, mouth wide open with fangs bared.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/血翼蝠_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: crimson red fuzzy body, dark red wing membranes, glowing yellow eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left in the air, wings bent but still spread with the same span as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a squeak, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/血翼蝠_睡著.png`
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

## 夜王蝠

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

**攻擊(可選)** → 存成 `art-src/夜王蝠_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: very dark purple body, black wing membranes with purple edges, glowing red eyes, white fangs, silver crown. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: swooping forward toward the right, wings spread with the same span as before.
Expression: angry and fierce, NOT smiling: brows slanted sharply down toward the center in a V shape, red eyes narrowed into a glare, mouth wide open with fangs bared.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/夜王蝠_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: very dark purple body, black wing membranes with purple edges, glowing red eyes, white fangs, silver crown. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: knocked backward toward the left in the air, wings bent but still spread with the same span as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a squeak, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/夜王蝠_睡著.png`
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

## 獅鷲獸

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

**攻擊(可選)** → 存成 `art-src/獅鷲獸_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden yellow beak, golden tan lion body, brown wings with lighter brown feather edges. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: rearing up on its hind legs facing right, front talons striking forward, wings raised half open as before (not wider).
Expression: angry and fierce: brow feathers slanted sharply down toward the center in a V shape, eagle eyes narrowed into a glare, beak wide open screeching.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/獅鷲獸_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden yellow beak, golden tan lion body, brown wings with lighter brown feather edges. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, head pulled back, wings half open as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/獅鷲獸_睡著.png`
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

## 獅鷲騎獸

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

**攻擊(可選)** → 存成 `art-src/獅鷲騎獸_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden beak, sky blue lion body, blue and white wings, silver armor with a brown leather saddle. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: rearing up on its hind legs facing right, front talons striking forward, wings raised half open as before (not wider).
Expression: angry and fierce: brow feathers slanted sharply down toward the center in a V shape, eagle eyes narrowed into a glare, beak wide open screeching.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/獅鷲騎獸_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head, golden beak, sky blue lion body, blue and white wings, silver armor with a brown leather saddle. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, head pulled back, wings half open as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/獅鷲騎獸_睡著.png`
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

## 皇家獅鷲

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

**攻擊(可選)** → 存成 `art-src/皇家獅鷲_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head with golden crest feathers, golden beak, golden-orange lion body, golden wings with white feather edges, red jewel ornaments. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: rearing up on its hind legs facing right, front talons striking forward, wings raised half open as before (not wider).
Expression: angry and fierce: brow feathers slanted sharply down toward the center in a V shape, eagle eyes narrowed into a glare, beak wide open screeching.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/皇家獅鷲_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: white eagle head with golden crest feathers, golden beak, golden-orange lion body, golden wings with white feather edges, red jewel ornaments. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, head pulled back, wings half open as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a cry.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/皇家獅鷲_睡著.png`
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

## 幼龍

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

**攻擊(可選)** → 存成 `art-src/幼龍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: orange scales, cream colored belly, ivory horns, orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: leaning forward toward the right and breathing a small puff of flame from its mouth, wings raised.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (the small flame coming from its mouth is the only effect allowed), only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/幼龍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: orange scales, cream colored belly, ivory horns, orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, tiny wings folded, tail curled.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/幼龍_睡著.png`
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

## 飛龍

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

**攻擊(可選)** → 存成 `art-src/飛龍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange scales, cream belly, ivory horns, red-orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: leaning forward toward the right and breathing a small puff of flame from its mouth, wings raised.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (the small flame coming from its mouth is the only effect allowed), only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/飛龍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: red-orange scales, cream belly, ivory horns, red-orange wings with lighter orange membranes, amber eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, tiny wings folded, tail curled.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/飛龍_睡著.png`
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

## 赤炎龍

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

**攻擊(可選)** → 存成 `art-src/赤炎龍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep crimson scales, orange belly, ivory horns, dark red wings with orange membranes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: leaning forward toward the right and breathing a small puff of flame from its mouth, wings raised.
Expression: angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (the small flame coming from its mouth is the only effect allowed), only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/赤炎龍_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep crimson scales, orange belly, ivory horns, dark red wings with orange membranes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: recoiling backward toward the left, tiny wings folded, tail curled.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/赤炎龍_睡著.png`
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

## 銀月狼

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

**攻擊(可選)** → 存成 `art-src/銀月狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: silver blue-gray fur with a pale blue belly and muzzle, white tail tip, bright blue eyes, white fangs, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/銀月狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: silver blue-gray fur with a pale blue belly and muzzle, white tail tip, bright blue eyes, white fangs, pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/銀月狼_睡著.png`
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

## 月影狼

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

**攻擊(可選)** → 存成 `art-src/月影狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lavender silver fur with violet shading, white tail tip, bright blue eyes, glowing pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/月影狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: lavender silver fur with violet shading, white tail tip, bright blue eyes, glowing pale yellow crescent moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/月影狼_睡著.png`
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

## 天狼

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

**攻擊(可選)** → 存成 `art-src/天狼_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: shining white fur with pale silver shading, pale blue sparkles in the tail, bright blue eyes, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: lunging forward toward the right with front paws off the ground, ears pinned forward.
Expression: angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/天狼_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: shining white fur with pale silver shading, pale blue sparkles in the tail, bright blue eyes, glowing golden full moon mark. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: flinching backward toward the left, ears flat against its head, tail tucked.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/天狼_睡著.png`
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

## 暮光鳥

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

**攻擊(可選)** → 存成 `art-src/暮光鳥_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dusky purple body with lavender shading, dark purple wings, tail feathers in orange, coral, magenta and indigo, golden beak, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open showing tiny fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/暮光鳥_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dusky purple body with lavender shading, dark purple wings, tail feathers in orange, coral, magenta and indigo, golden beak, red eyes, white fangs. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/暮光鳥_睡著.png`
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

## 夜虹鳥

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

**攻擊(可選)** → 存成 `art-src/夜虹鳥_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep plum body, indigo wings, tail feathers in magenta, violet and indigo with white star dots, golden beak, red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open showing tiny fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/夜虹鳥_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: deep plum body, indigo wings, tail feathers in magenta, violet and indigo with white star dots, golden beak, red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/夜虹鳥_睡著.png`
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

## 晨昏鳳凰

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

**攻擊(可選)** → 存成 `art-src/晨昏鳳凰_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: teal body; wings and tail fading from bright orange and gold to deep blue and purple; golden crest and beak; red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before.
Expression: angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open showing tiny fangs.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/晨昏鳳凰_受傷.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: teal body; wings and tail fading from bright orange and gold to deep blue and purple; golden crest and beak; red eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before.
Expression: in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/晨昏鳳凰_睡著.png`
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

## 炎龍(BOSS)

BOSS 只需要主圖和攻擊圖,不用 Q 版得那麼可愛。

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

**攻擊(可選)** → 存成 `art-src/炎龍_攻擊.png`
```
Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, outline thickness, art style and these exact colors: dark red scales, orange belly, ivory horns, black spikes, glowing yellow eyes. Do not add or remove any features.
Keep the character the same size as in the previous image. The character's widest or tallest side fills about 70% of the image.
Pose: rearing up and breathing a big stream of fire forward toward the right.
Expression: furious: eyes glowing and narrowed, jaws wide open.
Full body, still facing right (side view, three-quarter), centered.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, no motion lines or effects (the fire breath is the only effect allowed), only this one character.
Square image, 1024x1024.
```
