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

> 路線圖的安排:這階段只試做噗噗和小火妖;其他寵物等階段 3(繁殖與進化)定案後再全面產圖,避免畫完又改。
> 下面先把全部的 prompt 準備好,想提早畫也可以。

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
