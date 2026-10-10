# 繪圖 prompt 集(ChatGPT 直接複製貼上)

每一段都是完整的 prompt,不用拼湊。規格與流程見 `美術規格.md`。

## 怎麼用

1. **每隻寵物開一個新對話**。想讓畫風跟噗噗一樣,先把 `art-src/噗噗.png` 拖進對話(當參考圖),再貼「主圖」。
2. 主圖滿意後,**在同一個對話**依序貼「攻擊」「受傷」「睡著」(這三張可有可無)。
3. 每張下載後,照箭頭後面的檔名存到 `art-src/`,再開去背工具按「存進遊戲」。
4. 不滿意就直接用中文跟 GPT 說要改哪裡,例如「外框再粗一點」「眼睛大一點」。
5. GPT 偶爾會把灰白格子「畫」進圖裡(看起來透明其實不是)。遇到時把 `Background:` 那一行換成
   `Background: plain solid white background.`(白色系的寵物用 `plain solid bright green background`),去背工具會處理。

> 路線圖的安排:這階段只試做噗噗和小火妖;其他寵物等階段 3(繁殖與進化)定案後再全面產圖,避免畫完又改。
> 下面先把全部的 prompt 準備好,想提早畫也可以。

---

## 噗噗

試做。主圖你已經有了,動作圖請在產主圖的那個對話接著貼;對話不見了就先上傳 art-src/噗噗.png 再貼。

**主圖(必要)** → 存成 `art-src/噗噗.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a round pink jelly blob creature, glossy bouncy body, a small curled sprout on top, two small black oval eyes, tiny happy open-mouth smile.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: sitting still and happy, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/噗噗_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: squashed down and springing forward to body-slam, eyes narrowed with determination.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/噗噗_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: squished and recoiling backward, eyes squeezed shut, a small tear.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/噗噗_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: flattened and relaxed, eyes closed, sleeping peacefully.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 小火妖

試做。

**主圖(必要)** → 存成 `art-src/小火妖.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a small fire imp spirit, round red-orange body, wild hair made of yellow and orange flames, two tiny dark horns, big golden eyes, mischievous grin with a tiny fang, little stubby arms.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: floating in the air, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/小火妖_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: leaning forward in the air with both little hands thrust out, the flames of its hair flaring up.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/小火妖_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: knocked backward in the air, eyes squeezed shut, its hair flames shrinking.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/小火妖_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: floating curled up, eyes closed, its hair flames small and calm, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 綠史萊姆

**主圖(必要)** → 存成 `art-src/綠史萊姆.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a green slime creature, translucent droopy jelly body shaped like a water drop, two cute eyes, small bubbles inside its body.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: sitting still, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/綠史萊姆_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: stretching forward in a lunge with a determined face.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/綠史萊姆_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: wobbling backward, eyes squeezed shut.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/綠史萊姆_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: melted into a relaxed puddle shape, eyes closed, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 哥布林

**主圖(必要)** → 存成 `art-src/哥布林.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a small goblin, green skin, big pointy ears, yellow eyes, cheeky grin, brown leather tunic, holding a wooden club.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing ready, holding the club, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/哥布林_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: swinging the wooden club forward over its head, mouth open shouting.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/哥布林_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: stumbling backward holding its head, eyes squeezed shut.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/哥布林_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: sitting on the ground hugging the club, eyes closed, dozing.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 野狼

**主圖(必要)** → 存成 `art-src/野狼.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a gray wolf cub, fluffy fur, red eyes, small fangs, alert pointy ears, fierce but cute.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/野狼_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: lunging forward with mouth open showing fangs, front paws reaching out.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/野狼_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: flinching backward, ears flat, eyes squeezed shut.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/野狼_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: curled up lying down with its tail wrapped around, eyes closed, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 骷髏兵

白色系,如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。

**主圖(必要)** → 存成 `art-src/骷髏兵.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a cute chibi skeleton warrior, round skull with glowing red eye sockets, holding a rusty short sword and a small wooden shield.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing ready with sword and shield, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/骷髏兵_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: slashing forward with the rusty sword raised high.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/骷髏兵_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: bones rattling and leaning backward, skull tilted, eye glow flickering.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/骷髏兵_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: sitting slumped on the ground, eye glow dimmed, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 彩虹鴿

白色系,如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。

**主圖(必要)** → 存成 `art-src/彩虹鴿.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a white dove, round fluffy body, rainbow colored tail feathers (red, yellow, green, blue, purple), orange beak.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings flapping, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/彩虹鴿_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: diving forward with wings swept back and beak pointed.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/彩虹鴿_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: tumbling backward in the air, feathers ruffled, eyes squeezed shut.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/彩虹鴿_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: perched with its head tucked into its feathers, eyes closed, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 月狐

白色系,如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。

**主圖(必要)** → 存成 `art-src/月狐.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a pale moonlight fox, white and light blue fur, huge fluffy tail, bright blue eyes, pink inner ears, a small crescent moon mark on its forehead.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, tail held high, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/月狐_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: pouncing forward with front paws raised.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/月狐_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: flinching backward, ears flat, eyes squeezed shut.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/月狐_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: curled up with its huge fluffy tail wrapped around itself, eyes closed, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 吸血蝙蝠

**主圖(必要)** → 存成 `art-src/吸血蝙蝠.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a small purple vampire bat, big leathery wings, red eyes, two tiny white fangs, round fuzzy body.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: flying with wings spread open, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/吸血蝙蝠_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: swooping forward with fangs bared and wings swept back.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/吸血蝙蝠_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: knocked backward, wings crumpled, eyes squeezed shut.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/吸血蝙蝠_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: wrapped in its own wings like a cloak, eyes closed, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 獅鷲獸

頭是白色,如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。

**主圖(必要)** → 存成 `art-src/獅鷲獸.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a young griffin, white eagle head with golden beak, golden tan lion body, large brown feathered wings, lion tail.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing proudly with wings half open, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/獅鷲獸_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: rearing up with wings spread wide, beak open, front talons striking forward.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/獅鷲獸_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: recoiling backward with wings folded in, eyes squeezed shut.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/獅鷲獸_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: lying down with wings folded and head resting on its front legs, eyes closed, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 幼龍

**主圖(必要)** → 存成 `art-src/幼龍.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a baby dragon, orange scales, cream colored belly, two small ivory horns, small bat-like wings, big curious eyes, chubby.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on its hind legs, wings slightly open, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/幼龍_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: breathing a small puff of flame forward from its mouth, wings raised.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**受傷(可選)** → 存成 `art-src/幼龍_受傷.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: recoiling backward, eyes squeezed shut, tiny wings folded.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**睡著(可選)** → 存成 `art-src/幼龍_睡著.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: curled up with its tail around its body, eyes closed, a tiny smoke puff from its nose, sleeping.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

---

## 炎龍(BOSS)

BOSS 只需要主圖和攻擊圖,不用 Q 版得那麼可愛。

**主圖(必要)** → 存成 `art-src/炎龍.png`
```
If I attached a reference image, match its art style exactly (outline thickness, shading, colors), but draw the new character described below.
Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.
Character: a huge fierce red fire dragon, dark red scales, orange belly, large horns, spiky back, big wings spread, menacing glowing eyes, embers around it.
Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.
Pose: standing on four legs, wings spread wide, looking powerful, full body, side view facing right (three-quarter view), centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```

**攻擊(可選)** → 存成 `art-src/炎龍_攻擊.png`
```
Draw the exact same character as in the previous image (same design, colors, proportions, outline thickness and art style), now in this pose: rearing up and breathing a big stream of fire forward.
Full body, side view facing right, centered, with some empty space around it.
Background: transparent background (PNG). No shadow, no ground, no text, no extra objects or effects, only this one character.
Square image, 1024x1024.
```
