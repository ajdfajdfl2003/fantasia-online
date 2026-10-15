# -*- coding: utf-8 -*-
# 用法:python3.8 docs/art/gen_prompts.py docs/art/繪圖prompt.md
# 產生 docs/art/繪圖prompt.md:寵物 (主圖、攻擊、受傷、睡著)、主人、NPC、道具、登入畫面、地面材質、樹與裝飾的完整 prompt,
# 可直接貼到 ChatGPT
# 2026-10-11 修訂 (小火妖試做的教訓):
#   - 每隻寵物寫死配色 (Colors),重畫時顏色才不會飄
#   - 動作圖明講「不要重新設計、不要加減特徵、大小跟上一張一樣 (約佔寬度 70%)」
#   - 表情拆成 Pose / Expression 兩行,攻擊明講 NOT smiling,受傷用 > < 眼,睡著用往下彎的閉眼線
#   - 不再要求「火焰變小」之類會改變輪廓大小的描述
# 2026-10-11 階段 3:加入進化型態 (中階、高階) 與 2 種混種,共 39 個種族
#   - 進化型態的主圖要先上傳初階的圖當參考,動作圖沿用初階的姿勢
# 2026-10-15 階段 4 plan 第 6 項:加入主人、NPC、道具、登入畫面、地面材質、樹與裝飾 (spec 第 7~11 節)
#   - 初階 13 種與炎龍的動作圖改成必要,炎龍補受傷、睡著;中階、高階的動作圖可有可無
#   - 人物 2.5 頭身;女主人跟男版同配色、同帽子武器,換女版剪裁加長髮;髮色每個職業一種、男女同色
#   - 白色系 (牧師、修女等) 寫「沒給透明背景就改用純綠背景」:2026-10-14 假圖實測,米白、沒外框的身體會被當成背景去掉
#   - 道具名稱、登入畫面、地面、樹與裝飾的代號與中文檔名直接讀 game_data.py,跟遊戲同一份
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import game_data as G   # noqa: E402

OUT = sys.argv[1]

STYLE = ('Style: thick dark brown outline, flat cel shading with one shadow tone, soft glossy highlight, '
         'light from the upper left, vivid saturated colors, simple clean shapes that stay readable at small size.')
SIZE = "The character's widest or tallest side fills about 70% of the image."
RULES = ('Background: transparent background (PNG). No shadow, no ground, no text, no extra objects, '
         'no motion lines or effects%s, only this one character.\nSquare image, 1024x1024.')

# 表情的基本說法 (每隻可以覆寫)
ATK = ('angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, '
       'eyes narrowed into a glare, mouth wide open in a battle shout')
ATK_NOBROW = ('angry and fierce, NOT smiling: angry upper eyelids slanted down toward the center in a V shape, '
              'eyes narrowed into a glare, mouth wide open in a battle shout')
HURT = ('in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a wobbly cry, '
        'one small tear at the corner of an eye')
SLEEP = 'sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth small and relaxed, peaceful'

P = []


def pet(code, zh, desc, colors, pose, atk, hurt, sleep, note='', atk_face=ATK, hurt_face=HURT, sleep_face=SLEEP,
        atk_allow='', sleep_allow=''):
    P.append(dict(code=code, zh=zh, desc=desc, colors=colors, pose=pose, note=note,
                  frames=[('攻擊', atk, atk_face, atk_allow), ('受傷', hurt, hurt_face, ''), ('睡著', sleep, sleep_face, sleep_allow)]))


pet('poring', '噗噗', 'a round pink jelly blob creature with a glossy bouncy body, a small curled sprout on top, tiny round hands and feet, two small black oval eyes, a tiny happy open-mouth smile',
    'bubblegum pink body with lighter pink highlights and white shine spots, black eyes, dark brown outline',
    'sitting still and happy',
    'body squashed low and springing forward toward the right in a body-slam, the sprout on top bent backward',
    'body squished and tilted backward toward the left, tiny hands raised to its face, the sprout drooping',
    'body flattened and relaxed on the spot, the sprout drooping down',
    note='試做。主圖和三張動作圖都畫好了,這段留著以後重畫用。', atk_face=ATK_NOBROW)
pet('imp', '小火妖', 'a small floating fire imp spirit with a round chubby body, a big mane of wild hair made of flames, a small flame tail, two small curved horns, big golden eyes, a mischievous grin with one tiny fang, little stubby arms',
    'red-orange body; flame hair and flame tail with pale yellow-white centers, bright yellow middle and orange to red-orange tips; dark brown horns; golden yellow eyes',
    'floating in the air',
    'whole body leaning forward diagonally toward the right as if charging, both little arms thrust straight forward, the flame hair and flame tail streaming backward and keeping the same size',
    'knocked backward: body tilted back toward the left, arms flung up, the flame hair blown backward but keeping the same size',
    'floating curled up into a ball, arms tucked in, the flame hair resting calmly around it and keeping the same size',
    note='試做。主圖和三張動作圖都畫好了,這段留著以後重畫用。',
    atk_face='angry and fierce, NOT smiling: eyebrows slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth wide open in a battle shout showing the tiny fang')
pet('slime', '綠史萊姆', 'a green slime creature with a translucent droopy jelly body shaped like a water drop, two cute eyes, small bubbles inside its body',
    'translucent lime green body with lighter green highlights and white shine, darker green bubbles inside, black eyes',
    'sitting still',
    'body stretching forward toward the right in a lunge, the front of the body reaching out',
    'body wobbling and leaning backward toward the left, droopy',
    'body melted into a low relaxed puddle shape', atk_face=ATK_NOBROW)
pet('goblin', '哥布林', 'a small goblin with big pointy ears, yellow eyes, a cheeky grin, a brown leather tunic, holding a wooden club',
    'olive green skin, yellow eyes, brown leather tunic, light brown wooden club',
    'standing ready, holding the club',
    'stepping forward toward the right and swinging the wooden club down from over its head',
    'stumbling backward toward the left, one hand holding its head, the club lowered',
    'sitting on the ground with legs stretched out, hugging the club, head tilted to one side',
    sleep_face='sound asleep: eyes closed and drawn as gentle downward-curved lines, mouth slightly open with a little drool')
pet('wolf', '野狼', 'a wolf cub with fluffy fur, red eyes, small fangs, alert pointy ears, fierce but cute',
    'blue-gray fur with a light gray belly and muzzle, darker gray ear tips, red eyes, white fangs',
    'standing on four legs',
    'lunging forward toward the right with front paws off the ground, ears pinned forward',
    'flinching backward toward the left, ears flat against its head, tail tucked',
    'curled up lying down with its tail wrapped around its nose',
    atk_face='angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing',
    hurt_face='in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye')
pet('skeleton', '骷髏兵', 'a cute chibi skeleton warrior with a round skull and glowing eye sockets, holding a rusty short sword and a small wooden shield',
    'ivory white bones, glowing red eye sockets, rusty brown sword, brown wooden shield',
    'standing ready with sword and shield',
    'stepping forward toward the right and slashing with the rusty sword raised high, shield held in front',
    'knocked backward toward the left, bones knocked slightly askew, skull tilted, one arm flailing',
    'sitting slumped on the ground, the sword resting across its lap, skull drooping forward',
    note='白色系:如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。',
    atk_face='angry and fierce: the glowing red eye sockets narrowed into angry slanted slits forming a V, jaw wide open in a war cry',
    hurt_face='in shock: the eye glows shrunk to tiny dots, jaw hanging wide open',
    sleep_face='asleep: the eye glows dimmed to tiny faint dots, jaw slightly open, relaxed')
pet('dove', '彩虹鴿', 'a dove with a round fluffy body, a fan of rainbow colored tail feathers, an orange beak, flapping wings',
    'white body with pale gray wing shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes',
    'flying with wings flapping',
    'diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before',
    'tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before',
    'dozing while hovering in the air (it is a flying pet), head drooping onto its chest, wings spread in a slow glide with the same spread as before',
    note='白色系:如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。'
         '遊戲裡牠是飛在空中的,所以睡著也畫成在空中打瞌睡。動作圖大小:翅膀的張開程度會影響工具的自動對齊,存進遊戲前在工具預覽跟主圖比一下,必要時調「動作圖大小」。',
    atk_face='angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open in a battle cry',
    hurt_face='in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear')
pet('fox', '月狐', 'a moonlight fox with a huge fluffy tail, bright eyes, a small crescent moon mark on its forehead',
    'white fur with pale light-blue shading, bright blue eyes, pink inner ears, pale yellow crescent moon mark',
    'standing on four legs, tail held high',
    'pouncing forward toward the right with front paws raised, tail swept back',
    'flinching backward toward the left, ears flat, tail tucked',
    'curled up with its huge fluffy tail wrapped around its body like a blanket',
    note='白色系:如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。',
    atk_face='angry and fierce, NOT smiling: brow fur slanted sharply down toward the center in a V shape, eyes narrowed into a glare, mouth open showing small fangs')
pet('bat', '吸血蝙蝠', 'a small vampire bat with big leathery wings, two tiny fangs, a round fuzzy body',
    'purple fuzzy body, darker purple wing membranes, red eyes, white fangs',
    'flying with wings spread open',
    'swooping forward toward the right, wings spread with the same span as before',
    'knocked backward toward the left in the air, wings bent but still spread with the same span as before',
    'dozing while floating in the air (it is a flying pet), wings drooping but still spread with the same span as before',
    note='遊戲裡牠是飛在空中的,所以睡著也畫成在空中打瞌睡。動作圖大小:翅膀的張開程度會影響工具的自動對齊,存進遊戲前在工具預覽跟主圖比一下,必要時調「動作圖大小」。',
    atk_face='angry and fierce, NOT smiling: brows slanted sharply down toward the center in a V shape, red eyes narrowed into a glare, mouth wide open with fangs bared',
    hurt_face='in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a squeak, one small tear',
    sleep_face='sound asleep: eyes closed and drawn as gentle downward-curved lines, the two fangs peeking out')
pet('griffin', '獅鷲獸', 'a young griffin with an eagle head, a lion body, large feathered wings and a lion tail',
    'white eagle head, golden yellow beak, golden tan lion body, brown wings with lighter brown feather edges',
    'standing proudly with wings half open',
    'rearing up on its hind legs facing right, front talons striking forward, wings raised half open as before (not wider)',
    'recoiling backward toward the left, head pulled back, wings half open as before',
    'lying down with its head resting on its front legs, wings resting half open on its back as before',
    note='頭是白色:如果 GPT 沒給透明背景,把 Background 那行換成 plain solid bright green background。動作圖大小:翅膀的張開程度會影響工具的自動對齊,存進遊戲前在工具預覽跟主圖比一下,必要時調「動作圖大小」。',
    atk_face='angry and fierce: brow feathers slanted sharply down toward the center in a V shape, eagle eyes narrowed into a glare, beak wide open screeching',
    hurt_face='in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a cry')
pet('drake', '幼龍', 'a chubby baby dragon with two small horns, small bat-like wings and big curious eyes',
    'orange scales, cream colored belly, ivory horns, orange wings with lighter orange membranes, amber eyes',
    'standing on its hind legs, wings slightly open',
    'leaning forward toward the right and breathing a small puff of flame from its mouth, wings raised',
    'recoiling backward toward the left, tiny wings folded, tail curled',
    'curled up with its tail around its body',
    note='攻擊圖的火焰會讓面積變大,工具自動對齊後可能偏小,存進遊戲前在預覽跟主圖比一下,必要時調「動作圖大小」。',
    atk_allow=' (the small flame coming from its mouth is the only effect allowed)',
    sleep_allow=' (a tiny smoke puff from its nose is the only effect allowed)',
    sleep_face='sound asleep: eyes closed and drawn as gentle downward-curved lines, a tiny smoke puff from its nose')
pet('silverwolf', '銀月狼', 'a silver moon wolf cub, a hybrid of a wolf and a moon fox, with silver-blue fur, a fluffy fox-like tail, alert pointy ears and a small crescent moon mark on its forehead',
    'silver blue-gray fur with a pale blue belly and muzzle, white tail tip, bright blue eyes, white fangs, pale yellow crescent moon mark',
    'standing on four legs, tail held high',
    'lunging forward toward the right with front paws off the ground, ears pinned forward',
    'flinching backward toward the left, ears flat against its head, tail tucked',
    'curled up lying down with its fluffy tail wrapped around its nose',
    note='混種(野狼 × 月狐,只能配對得到)。想讓牠像爸媽,可以把 art-src/野狼.png 和 art-src/月狐.png 一起上傳當參考。',
    atk_face='angry and fierce, NOT smiling: brow fur slanted sharply down toward the center, eyes narrowed into a glare, mouth wide open snarling with fangs showing',
    hurt_face='in pain: eyes squeezed tightly shut and drawn as > < shapes, mouth open in a whimper, one small tear at the corner of an eye')
pet('duskbird', '暮光鳥', 'a twilight bird, a hybrid of a rainbow dove and a vampire bat, with a round fluffy body, feathered wings with small bat-like claws at the tips, a sunset colored tail fan and two tiny fangs',
    'dusky purple body with lavender shading, dark purple wings, tail feathers in orange, coral, magenta and indigo, golden beak, red eyes, white fangs',
    'flying with wings flapping',
    'diving forward toward the right in the air, beak pointed forward, wings raised behind it with the same spread as before',
    'tumbling backward toward the left in the air, feathers ruffled, wings flung up with the same spread as before',
    'dozing while hovering in the air (it is a flying pet), head drooping onto its chest, wings spread in a slow glide with the same spread as before',
    note='混種(彩虹鴿 × 吸血蝙蝠,只能配對得到)。可以把 art-src/彩虹鴿.png 和 art-src/吸血蝙蝠.png 一起上傳當參考。'
         '會飛的寵物,睡著也畫成在空中打瞌睡。',
    atk_face='angry and fierce, NOT cute-smiling: brow feathers slanted sharply down toward the center in a V shape, eyes narrowed into a glare, beak open showing tiny fangs',
    hurt_face='in pain: eyes squeezed tightly shut and drawn as > < shapes, beak open in a squawk, one small tear')

# 進化型態:初階代號 → ((中階描述, 中階配色), (高階描述, 高階配色));名字和代號跟 game_data.FORMS 一致
EVO = {
    'poring': (('a bigger round jelly blob creature with a glossy bouncy body, two curled sprouts on top, small round hands and feet, determined black oval eyes and a confident smile',
                'lilac purple-pink body with lighter pink highlights and white shine spots, green sprouts, black eyes, dark brown outline'),
               ('a large majestic round jelly blob king with a glossy body, a small golden crown on top, a short red royal cape, tiny round hands and feet, proud black eyes and a confident smile',
                'warm golden orange jelly body with light yellow highlights and white shine spots, golden crown with red jewels, red cape with white trim, black eyes')),
    'slime': (('a big slime creature with a translucent wobbly jelly body shaped like a large water drop, two cute eyes, many bubbles inside and a small swirl on top',
               'translucent teal body with light aqua highlights and white shine, darker teal bubbles inside, black eyes'),
              ('a huge slime king with a translucent jelly body, a small golden crown floating on top, two confident eyes and glowing bubbles inside',
               'translucent violet-blue body with light lavender highlights and white shine, glowing pale blue bubbles, golden crown, black eyes')),
    'goblin': (('a goblin warrior, taller and more muscular, with big pointy ears, a leather helmet, studded leather armor and a wooden club with iron spikes',
                'olive green skin, yellow eyes, dark brown leather helmet and armor with iron studs, wooden club with gray iron spikes'),
               ('a goblin chieftain with big pointy ears, a feathered tribal headdress, a fur cloak, war paint stripes on its cheeks and a big bone-and-stone war club',
                'olive green skin, yellow eyes, red and white headdress feathers, brown fur cloak, red war paint, ivory bone club')),
    'wolf': (('a young wind wolf, sleek and fast-looking, with longer legs, fur swept back like wind, sharp ears and a bushy tail',
              'sage green-gray fur with a pale gray belly, darker green streaks like wind, red eyes, white fangs'),
             ('a majestic wolf king, large and powerful, with a thick mane of fur around its neck, a small scar over one eye, sharp fangs and a proud stance',
              'jet black fur with dark gray highlights, silver mane tips, glowing red eyes, white fangs')),
    'skeleton': (('a skeleton knight wearing a dented steel helmet and a breastplate, holding a longsword and a round shield',
                  'ivory white bones, glowing red eye sockets, bluish steel helmet and breastplate, silver longsword, blue round shield'),
                 ('a skeleton general wearing an ornate golden helmet with a red plume, golden armor and a tattered red cape, holding a big curved greatsword',
                  'ivory white bones, glowing red eye sockets, golden helmet and armor, red plume and cape, silver greatsword')),
    'imp': (('a bigger floating fire imp with a mane of wild flames, longer curved horns, a flame tail, sharp golden eyes, a mischievous fanged grin and little clawed arms',
             'deep red body; flame hair and flame tail with yellow-white centers, orange middle and crimson tips; dark brown horns; golden eyes'),
            ('a floating flame demon lord with a crown of blue flames, big curved horns, small bat-like wings, a flame tail, glowing eyes and a confident grin',
             'dark navy-purple body; blue flames with white centers and cyan to deep blue tips; black horns; glowing white-blue eyes')),
    'dove': (('a radiant dove, larger, with longer elegant wings, a small feather crest and a long fan of shimmering rainbow tail feathers',
              'cream white body with warm golden shading, tail feathers in red, yellow, green, blue and purple, orange beak, black eyes'),
             ('a celestial rainbow bird, majestic, with large wings, a long flowing tail of rainbow feathers, a golden feather crest and a small halo of light above its head',
              'golden yellow body with white highlights, rainbow tail feathers, golden crest, pale yellow halo, orange beak, black eyes')),
    'fox': (('a snow moon fox, larger, with two fluffy tails, frosty fur tufts and a brighter crescent moon mark on its forehead',
             'white fur with icy blue shading, light blue tail tips, bright blue eyes, pink inner ears, silver crescent moon mark'),
            ('an elegant nine-tailed moon fox with nine flowing fluffy tails fanned behind it and a glowing full moon mark on its forehead',
             'cream white fur with warm golden shading, golden tail tips, golden eyes, pink inner ears, glowing golden full moon mark')),
    'bat': (('a blood-wing bat, larger, with jagged leathery wings, sharper fangs and tall pointy ears',
             'crimson red fuzzy body, dark red wing membranes, glowing yellow eyes, white fangs'),
            ('a regal night king bat with huge leathery wings, a high fur collar like a vampire cape, sharp fangs and a tiny silver crown',
             'very dark purple body, black wing membranes with purple edges, glowing red eyes, white fangs, silver crown')),
    'griffin': (('an armored griffin steed, larger, wearing a light saddle and a steel chest plate, with large feathered wings',
                 'white eagle head, golden beak, sky blue lion body, blue and white wings, silver armor with a brown leather saddle'),
                ('a royal griffin, majestic, with huge golden-feathered wings, a royal crest of feathers on its head and golden ornaments on its chest',
                 'white eagle head with golden crest feathers, golden beak, golden-orange lion body, golden wings with white feather edges, red jewel ornaments')),
    'drake': (('a young wyvern, slimmer and taller than a baby dragon, with larger wings, longer horns and a longer tail',
               'red-orange scales, cream belly, ivory horns, red-orange wings with lighter orange membranes, amber eyes'),
              ('a crimson flame dragon, powerful but still chibi, with big horns, a spiky back, large wings and embers glowing between its scales',
               'deep crimson scales, orange belly, ivory horns, dark red wings with orange membranes, glowing yellow eyes')),
    'silverwolf': (('a moon shadow wolf, sleek, with flowing silver-violet fur, a fluffy tail and a glowing crescent moon mark',
                    'lavender silver fur with violet shading, white tail tip, bright blue eyes, glowing pale yellow crescent moon mark'),
                   ('a celestial wolf, majestic, with flowing white fur like starlight, a long fluffy tail with tiny sparkles and a glowing full moon mark',
                    'shining white fur with pale silver shading, pale blue sparkles in the tail, bright blue eyes, glowing golden full moon mark')),
    'duskbird': (('a night rainbow bird, larger, with long wings and a long tail in night-sky colors dotted with tiny stars',
                  'deep plum body, indigo wings, tail feathers in magenta, violet and indigo with white star dots, golden beak, red eyes'),
                 ('a dawn and dusk phoenix, majestic, with large wings whose feathers fade from sunrise orange to night blue, a long flowing tail and a feather crest',
                  'teal body; wings and tail fading from bright orange and gold to deep blue and purple; golden crest and beak; red eyes')),
}
FORM_NAMES = {   # 跟 game_data.FORMS 一樣
    'poring': ('彈彈噗', '噗噗國王'), 'slime': ('大史萊姆', '史萊姆王'), 'goblin': ('哥布林戰士', '哥布林酋長'),
    'wolf': ('疾風狼', '狼王'), 'skeleton': ('骷髏騎士', '骷髏將軍'), 'imp': ('火妖', '炎魔'), 'dove': ('虹光鴿', '天虹鳥'),
    'fox': ('雪月狐', '九尾月狐'), 'bat': ('血翼蝠', '夜王蝠'), 'griffin': ('獅鷲騎獸', '皇家獅鷲'), 'drake': ('飛龍', '赤炎龍'),
    'silverwolf': ('月影狼', '天狼'), 'duskbird': ('夜虹鳥', '晨昏鳳凰'),
}


def forms_of(base):
    """初階 → [中階, 高階] 的 prompt 資料:姿勢、動作沿用初階"""
    out = []
    for st, ((desc, colors), zh) in enumerate(zip(EVO[base['code']], FORM_NAMES[base['code']])):
        out.append(dict(base, code=base['code'] + str(st + 2), zh=zh, desc=desc, colors=colors, stage=st + 1, base_zh=base['zh'],
                        note='%s(%s的%s)。開新對話,先把 `art-src/%s.png` 上傳當參考圖,再貼主圖。'
                             % ('中階' if st == 0 else '高階', base['zh'], '第二階' if st == 0 else '最終型態', base['zh'])))
    return out


BOSS = dict(code='dragon', zh='炎龍(BOSS)', desc='a huge fierce fire dragon with large horns, a spiky back, big wings spread and menacing glowing eyes, embers around it',
            colors='dark red scales, orange belly, ivory horns, black spikes, glowing yellow eyes',
            pose='standing on four legs, wings spread wide, looking powerful',
            note='BOSS 不用畫得那麼可愛。攻擊、受傷、睡著三張動作圖都是必要的(spec 第 1 節)。'
                 '翅膀的張開程度會影響工具的自動對齊,批次的縮圖看起來身體跟主圖不一樣大,就點縮圖進單張模式調「動作圖大小」。',
            frames=[('攻擊', 'rearing up and breathing a big stream of fire forward toward the right',
                     'furious: eyes glowing and narrowed, jaws wide open', ' (the fire breath is the only effect allowed)'),
                    ('受傷', 'recoiling backward toward the left, head pulled back, wings still spread wide as before',
                     'in pain: eyes squeezed tightly shut, jaws open in a roar of pain', ''),
                    ('睡著', 'lying down on its belly with its head resting on its front legs, wings resting half open on its back',
                     'sound asleep: eyes closed and drawn as gentle downward-curved lines, a tiny smoke puff from its nostrils',
                     ' (a tiny smoke puff from its nostrils is the only effect allowed)')])


def main_prompt(p):
    return ('If I attached a reference image, match its art style exactly (outline thickness, shading, colors), '
            'but draw the new character described below.\n'
            'Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.\n'
            'Character: %s.\nColors: %s.\n%s\n'
            'Pose: %s, full body, side view facing right (three-quarter view), centered. %s\n%s'
            % (p['desc'], p['colors'], STYLE, p['pose'], SIZE, RULES % ''))


def evo_prompt(p):
    return ('The attached image shows the first form of this creature line. Draw its %s: '
            'keep it clearly recognizable as the same creature line and match the art style exactly (outline thickness, shading), '
            'but make it look %s.\n'
            'Create a game sprite of a cute chibi fantasy creature for a 2000s Taiwanese MMORPG pet game.\n'
            'Character: %s.\nColors: %s.\n%s\n'
            'Pose: %s, full body, side view facing right (three-quarter view), centered. %s\n%s'
            % ('evolved form (second stage)' if p['stage'] == 1 else 'final evolved form (third stage)',
               'more grown-up and stronger' if p['stage'] == 1 else 'majestic and powerful, but still cute chibi',
               p['desc'], p['colors'], STYLE, p['pose'], SIZE, RULES % ''))


def frame_prompt(p, pose, face, allow):
    return ('Draw the exact same character as in the previous image. Do not redesign it: keep the same design, proportions, '
            'outline thickness, art style and these exact colors: %s. Do not add or remove any features.\n'
            'Keep the character the same size as in the previous image. %s\n'
            'Pose: %s.\n'
            'Expression: %s.\n'
            'Full body, still facing right (side view, three-quarter), centered.\n%s'
            % (p['colors'], SIZE, pose, face, RULES % allow))


def block(title, fname, prompt):
    return '**%s** → 存成 `art-src/%s`\n```\n%s\n```\n' % (title, fname, prompt)


# ============================================================
#  人物、道具、登入畫面、地面、樹與裝飾 (階段 4 plan 第 6 項,spec 第 7~11 節)
# ============================================================
GREEN_BG = ('沒給透明背景就改用純綠背景(把 `Background:` 那一行換成 `Background: plain solid bright green background.`)。'
            '2026-10-14 用假圖實測,米白色、沒有外框的身體會被當成背景去掉。')
CHIBI = ('Proportions: chibi, 2.5 heads tall (the head is about 40% of the total height), big expressive eyes, '
         'the face and hairstyle clearly readable. In the game the character is only about 52 pixels tall, '
         'so keep the shapes bold and simple.')
PEOPLE_STYLE = '(2.5 heads tall proportions, outline thickness, shading, face style)'

# 主人:5 職業 × 男女 (spec 第 7 節)。配色沿用程式繪圖 (sprites.js 的 CLASS_LOOK);
# 髮色每個職業一種、男女同色 (2026-10-15 與使用者確認):騎士栗棕、獵人銅紅、牧師黑、法師銀紫、吟遊詩人金
OWNERS = [
    dict(cls='knight', en='knight',
         m='a young male knight wearing an open-faced silver helmet topped with a red plume, a blue tunic over light silver armor '
           '(shoulder guards and a chest plate), brown trousers and dark brown boots, holding a silver sword and a round silver shield '
           'with a red emblem; short chestnut brown hair showing under the helmet',
         f='a young female knight wearing the same open-faced silver helmet topped with a red plume, long chestnut brown hair flowing '
           'out from under the helmet down her back with one lock framing her face, a blue tunic top over the same light silver armor '
           '(shoulder guards and a chest plate), a short armored skirt of silver plates over a blue skirt, dark brown knee-high boots, '
           'holding the same silver sword and the same round silver shield with a red emblem',
         cm='royal blue tunic, shiny silver helmet, armor and shield, red plume and red shield emblem, golden sword hilt, '
            'brown trousers, dark brown boots, chestnut brown hair, light peach skin, dark brown eyes',
         cf='royal blue tunic and skirt, shiny silver helmet, armor, armored skirt and shield, red plume and red shield emblem, '
            'golden sword hilt, dark brown boots, chestnut brown hair, light peach skin, dark brown eyes',
         pose='standing confidently, the sword held down at the side, the shield on the other arm',
         cast='raising the sword straight up above the head with one arm as if rallying allies, the shield held in front'),
    dict(cls='hunter', en='hunter',
         m='a young male hunter wearing a dark green cap with a white feather that has a red tip, a green hunting jacket with a brown '
           'leather belt, brown trousers and brown leather boots, holding a wooden longbow; short copper red hair',
         f='a young female hunter wearing the same dark green cap with a white feather that has a red tip, long copper red hair '
           'flowing down her back with one lock framing her face, the same green hunting jacket with a brown leather belt, '
           'short brown shorts, brown leather knee-high boots, holding the same wooden longbow',
         cm='leaf green jacket, dark green cap, white feather with a red tip, brown belt, trousers and boots, light brown wooden bow, '
            'copper red hair, light peach skin, dark brown eyes',
         cf='leaf green jacket, dark green cap, white feather with a red tip, brown belt, shorts and boots, light brown wooden bow, '
            'copper red hair, light peach skin, dark brown eyes',
         pose='standing relaxed, holding the bow at the side in one hand',
         cast='holding the bow up high in one hand and pointing forward toward the right with the other hand as if giving a command'),
    dict(cls='priest', en='priest',
         m='a young male priest wearing a tall white priest hat with a golden band and a small golden cross, a long white robe '
           'with a golden cross on the chest and golden trim at the hem and sleeves, holding a holy staff (a cream white staff '
           'topped with a golden cross); short black hair',
         f='a young female priest wearing the same tall white priest hat with a golden band and a small golden cross, long black hair '
           'flowing down her back with one lock framing her face, a white robe dress with a fitted waist tied by a golden sash and '
           'a flared skirt, the same golden cross on the chest and golden trim, holding the same holy staff',
         cm='white robe and hat with light warm gray shading, golden cross, band and trim, cream white staff with a golden cross, '
            'black hair, light peach skin, dark brown eyes',
         cf='white robe dress and hat with light warm gray shading, golden cross, band, sash and trim, cream white staff with '
            'a golden cross, black hair, light peach skin, dark brown eyes',
         extra='The white robe and hat need the same thick dark brown outline as everything else.',
         pose='standing calmly, holding the holy staff upright beside the body',
         cast='raising the holy staff high above the head with both hands as if calling down a blessing'),
    dict(cls='mage', en='mage',
         m='a young male mage wearing a tall dark purple pointed wizard hat with a golden band, a long purple robe with golden trim, '
           'holding a wooden staff topped with a round light blue crystal; short silver-lavender hair',
         f='a young female mage wearing the same tall dark purple pointed wizard hat with a golden band, long silver-lavender hair '
           'flowing down her back with one lock framing her face, a purple robe dress with a fitted waist and a flared skirt to just '
           'below the knees, golden trim, dark brown short boots, holding the same wooden staff topped with a round light blue crystal',
         cm='purple robe, dark purple hat, golden band and trim, brown wooden staff, light blue crystal, silver-lavender hair, '
            'light peach skin, dark brown eyes',
         cf='purple robe dress, dark purple hat, golden band and trim, dark brown boots, brown wooden staff, light blue crystal, '
            'silver-lavender hair, light peach skin, dark brown eyes',
         pose='standing confidently, holding the crystal staff upright beside the body',
         cast='holding the crystal staff out in front toward the right with both hands, the crystal pointing forward'),
    dict(cls='bard', en='bard',
         m='a young male bard wearing a dark blue cap with a long yellow feather, a red tunic with a golden sash across the chest, '
           'dark indigo trousers and brown boots, holding a wooden lute; short golden blonde hair',
         f='a young female bard wearing the same dark blue cap with a long yellow feather, long golden blonde hair flowing down her '
           'back with one lock framing her face, a red tunic dress with a short flared skirt and the same golden sash across the chest, '
           'dark indigo leggings and brown boots, holding the same wooden lute',
         cm='red tunic, golden yellow sash, dark blue cap, yellow feather, dark indigo trousers, brown boots, warm brown wooden lute, '
            'golden blonde hair, light peach skin, dark brown eyes',
         cf='red tunic dress, golden yellow sash, dark blue cap, yellow feather, dark indigo leggings, brown boots, '
            'warm brown wooden lute, golden blonde hair, light peach skin, dark brown eyes',
         pose='standing cheerfully, holding the lute in front of the body',
         cast='strumming the lute energetically, head tilted back',
         cast_face='singing happily, mouth wide open, eyes closed in joy'),
]
CAST_FACE = 'focused and determined, eyebrows raised, mouth open as if calling out'
CAST_FX = ' (no glow, no sparkles, no magic circles, no music notes: the game draws the spell light itself)'


def owner_prompt(o, sex):
    if o['cls'] == 'knight' and sex == 'm':
        ref = ('If I attached a reference image (a pet from the same game), match its art style exactly '
               '(outline thickness, shading, colors), but draw the human character described below. '
               'This character will be the style reference for all other human characters of the game.\n')
    elif sex == 'm':
        ref = ('The attached image is the male knight from the same game. Match its art style exactly %s, '
               'but draw the new character described below.\n' % PEOPLE_STYLE)
    elif o['cls'] == 'knight':
        ref = ('The attached image is the male knight from the same game. Draw the female version of this knight: '
               'match the art style exactly %s, keep the same outfit colors, the same helmet and the same weapons, '
               'only change the clothing cut to a female version and give her long hair.\n' % PEOPLE_STYLE)
    else:
        ref = ('I attached two images from the same game: first the male knight, then the male %s. '
               'Match their art style exactly %s. Draw the female version of the %s: keep the same outfit colors, '
               'the same hat and the same weapon as the male %s, only change the clothing cut to a female version '
               'and give her long hair.\n' % (o['en'], PEOPLE_STYLE, o['en'], o['en']))
    return (ref + 'Create a game sprite of a cute chibi human character for a 2000s Taiwanese MMORPG pet game: '
            'a player character (a pet trainer).\n%s\nCharacter: %s.\nColors: %s.\n%s\n%s'
            'Pose: %s, full body, side view facing right (three-quarter view), centered, the face clearly visible. %s\n%s'
            % (CHIBI, o[sex], o['c' + sex], STYLE, o['extra'] + '\n' if o.get('extra') else '', o['pose'], SIZE, RULES % ''))


def owner_cast_prompt(o, sex):
    return ('Draw the exact same character as in the previous image. Do not redesign it: keep the same design, '
            'proportions (2.5 heads tall), outline thickness, art style and these exact colors: %s. '
            'Do not add or remove any features.\n'
            'Keep the character the same size as in the previous image. %s\n'
            'Pose: casting a support spell: %s. Keep the body upright, do not lean (the game tilts the sprite forward by itself).\n'
            'Expression: %s.\n'
            'Full body, still facing right (side view, three-quarter), centered.\n%s'
            % (o['c' + sex], SIZE, o['cast'], o.get('cast_face', CAST_FACE), RULES % CAST_FX))


# NPC (spec 第 8 節):名字跟 server.py 的 NPCS 一樣;原圖檔名用名字的最後一段 (艾倫.png),也接受「村長 艾倫.png」
NPC_ART = [
    dict(zh='村長 艾倫', pet='poring', pet_en='poring (a pink jelly blob)', white=True,
         desc='a short and stout old dwarf, the village elder: a big white beard braided into two braids, bushy white eyebrows, '
              'rosy cheeks, a green shirt under a brown leather vest, brown trousers and boots, leaning on an oak walking stick; '
              'a small poring (the pet from the second reference image) sits on top of his head',
         colors='green shirt, brown leather vest, brown trousers and boots, white beard, hair and eyebrows with light gray shading, '
                'oak brown walking stick, light peach skin with rosy cheeks'),
    dict(zh='道具商人 莉莉', pet='slime', pet_en='green slime',
         desc='a cheerful young cat-eared girl, the item merchant: short orange hair, orange cat ears and a cat tail, a green merchant '
              'vest over a cream shirt, a big backpack on her back hung with bottles and jars, holding a red potion in one hand; '
              'a green slime (the pet from the second reference image) lies on top of the backpack',
         colors='orange hair, ears and tail, green vest, cream shirt, brown leather backpack, colorful glass bottles and jars, '
                'red potion, light peach skin'),
    dict(zh='修女 瑪莉', pet='dove', pet_en='rainbow dove', white=True,
         desc='a gentle young human nun: long golden blonde hair, a white and blue nun habit with a veil, holding a holy book with '
              'both hands; a rainbow dove (the pet from the second reference image) perches on her shoulder',
         colors='white habit with blue panels, blue veil with white trim, golden blonde hair, brown holy book with golden corners, '
                'light peach skin',
         extra='The white habit needs the same thick dark brown outline as everything else.'),
    dict(zh='傳送師 奧茲', pet='fox', pet_en='moon fox', white=True,
         desc='an elegant elf, the teleporter: long silver-white hair, long pointed elf ears, a deep blue robe and a pointed hat '
              'decorated with small stars like a starry night sky, holding a staff topped with a shining blue crystal '
              '(a painted highlight only, no glow around it); a moon fox (the pet from the second reference image) is draped '
              'around the shoulders like a scarf',
         colors='deep navy blue robe and hat with small pale yellow stars, silver-white hair, brown wooden staff, bright blue crystal, '
                'light peach skin'),
    dict(zh='孵化屋 葛莉絲婆婆', pet='imp', pet_en='fire imp', white=True,
         desc='a small, kind old rabbit-eared grandma: gray-white floppy rabbit ears, gray-white hair, round glasses, a long purple '
              'robe, carrying a basket full of eggs on one arm; a fire imp (the pet from the second reference image) sits inside '
              'the basket hugging an egg to keep it warm',
         colors='gray-white ears and hair, purple robe, round glasses with thin brown frames, light brown woven basket, '
                'cream and pastel colored eggs, light peach skin'),
    dict(zh='寵物旅館 蘿絲', pet='drake', pet_en='baby dragon',
         desc='a cheerful young dog-eared girl, the pet hotel keeper: reddish-brown twin tails, floppy dog ears, a pink dress with '
              'a white apron, holding a baby dragon (the pet from the second reference image) in her arms',
         colors='reddish-brown hair and dog ears, pink dress, white apron, brown shoes, light peach skin'),
]
PET_BY_CODE = {p['code']: p for p in P}
NPC_RULES = RULES.replace('only this one character', 'only this character and its pet')


def npc_prompt(n):
    return ('I attached two reference images from the same game: first the male knight (a human character), then the pet %s. '
            "Match the knight's art style exactly %s, and draw the pet exactly like its reference (same design and colors), "
            'small, as a companion.\n'
            'Create a game sprite of a cute chibi NPC (a non-player character) for a 2000s Taiwanese MMORPG pet game.\n'
            '%s\nCharacter: %s.\nColors: %s; the pet: %s.\n%s\n%s'
            "The pet must touch and overlap the character's body with no gap between them, "
            'so the character and the pet form one connected shape.\n'
            'Pose: standing, full body, side view facing right (three-quarter view), centered, the face clearly visible. '
            'The widest or tallest side of the whole sprite (the character and the pet together) fills about 70%% of the image.\n%s'
            % (n['pet_en'], PEOPLE_STYLE, CHIBI, n['desc'], n['colors'], PET_BY_CODE[n['pet']]['colors'], STYLE,
               n['extra'] + '\n' if n.get('extra') else '', NPC_RULES % ''))


# 道具 16 張 (spec 第 9 節):成品 64×64、置中;6 種蛋各長不一樣,看得出是哪種寵物的蛋
ITEM_ART = {
    'red_potion': ('a round glass potion bottle with a cork stopper, filled with bright red liquid',
                   'bright red liquid, clear glass with a light blue tint and a white shine, light brown cork'),
    'blue_potion': ('a round glass potion bottle with a cork stopper, filled with bright blue liquid',
                    'bright blue liquid, clear glass with a light blue tint and a white shine, light brown cork'),
    'revive_herb': ('a small bundle of a magical healing herb: a few bright green leaves on a short stem with one tiny white flower bud',
                    'bright green leaves with lighter green veins, white flower bud with a pale yellow center'),
    'seal_card': ('a magic sealing card: a rectangular card with rounded corners, tilted slightly, with a simple golden magic circle '
                  'pattern on it (only shapes, no letters or symbols that look like writing)',
                  'lavender purple card, golden border and pattern, white highlight'),
    'egg_imp': ('a pet egg, oval and standing upright, with yellow flame-shaped patterns rising from the bottom (the egg of a little fire imp)',
                'red-orange shell with a white shine, yellow and orange flame patterns'),
    'egg_dove': ('a pet egg, oval and standing upright, with soft rainbow stripes wrapping around its middle (the egg of a rainbow dove)',
                 'white shell with pale gray shading, stripes in red, yellow, green, blue and purple'),
    'egg_fox': ('a pet egg, oval and standing upright, with a crescent moon mark and a few tiny stars (the egg of a moon fox)',
                'pale icy blue shell with a white shine, pale yellow crescent moon and stars'),
    'egg_bat': ('a pet egg, oval and standing upright, with a dark bat-wing pattern on its sides (the egg of a vampire bat)',
                'dark purple shell with a lighter purple shine, black bat-wing pattern, a few small red spots'),
    'egg_griffin': ('a pet egg, oval and standing upright, with brown feather-shaped speckles (the egg of a griffin)',
                    'golden tan shell with a white shine, brown feather patterns'),
    'egg_drake': ('a pet egg, oval and standing upright, covered in a scale pattern, with two tiny horn-like bumps on top '
                  '(the egg of a baby dragon)',
                  'orange shell with a darker orange scale pattern and cream highlights, ivory bumps'),
    'meat': ('a fresh raw meat steak on a bone, cartoon style', 'red-pink meat with light pink marbling, ivory bone'),
    'fish': ('a fresh whole fish lying on its side, cartoon style', 'blue back fading to a silver-white belly, light blue fins, black eye'),
    'berry': ('a small cluster of round wild berries with two green leaves', 'magenta-purple berries with white shine spots, green leaves'),
    'wheat': ('three golden ears of wheat tied together with a string', 'golden yellow wheat, light brown string'),
    'wood': ('a small bundle of three firewood logs tied with a rope', 'brown bark, light tan cut ends with tree rings, beige rope'),
    'ore': ('a rough chunk of rock ore with shiny crystals sticking out of it', 'blue-gray rock, sparkling light blue and silver crystals'),
}


def item_prompt(desc, colors):
    return ('If I attached a reference image, match its art style exactly (outline thickness, shading, colors), '
            'but draw the item described below.\n'
            'Create a game item icon for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.\n'
            'Item: %s.\nColors: %s.\n%s\n'
            'View: one single item, seen slightly from the front and above, centered, filling about 80%% of the image. '
            'In the game it is shown only 32 pixels wide, so keep a bold, simple and clear silhouette.\n'
            'Background: transparent background (PNG). No shadow, no ground, no text, no letters, no numbers, '
            'no frame or border, no glow or sparkles, no extra objects, only this one item.\nSquare image, 1024x1024.'
            % (desc, colors, STYLE))


# 登入畫面 (spec 第 10 節):主視覺左邊男騎士、右邊女牧師;Logo 只畫中文,英文維持網頁字 (2026-10-15 與使用者確認)
LOGIN_PROMPT = (
    'I attached six reference images from the same game, in this order: the male knight, the female priest, the pet poring '
    '(a pink jelly blob), the pet fire imp, the pet wolf cub and the pet rainbow dove. Draw all of them exactly like their '
    'references (same designs and colors) and match their art style.\n'
    'Create the title screen key art for a 2000s Taiwanese MMORPG pet game, in a bright fairy-tale adventure mood.\n'
    'Scene: a sunny blue sky with big fluffy white clouds over a green rolling meadow with a few flowers, a small cozy village '
    'with red roofs in the middle distance, and far away to the north a volcano with the dark silhouette of a huge fire dragon on top of it.\n'
    'Foreground: the male knight on the left side and the female priest on the right side, both happy and ready for an adventure; '
    'the poring and the wolf cub near the knight, the fire imp floating near the priest, the rainbow dove flying in the sky above them.\n'
    'Composition: keep the center of the image calm and open (only sky and meadow, no characters and no important details there): '
    'a login box will cover about the middle 35% of the width and most of the height. Put the characters only in the left and '
    'right thirds of the image.\n'
    'Style: the characters keep the same thick dark brown outlines and cel shading as the references; the background is softer '
    'and more painterly, with lighter outlines, so the characters stand out.\n'
    'No text, no logo, no letters, no user interface, no frame or border.\n'
    'Landscape image, 1536x1024.')
LOGO_PROMPT = (
    'Create a game title logo for a 2000s Taiwanese MMORPG pet game.\n'
    'Text: exactly these four Traditional Chinese characters on one line, from left to right: 幻想之境 (幻, 想, 之, 境). '
    'Draw every stroke of each character correctly. No other text: no English, no extra characters, no subtitle.\n'
    'Lettering: bold brush-calligraphy style characters (like kaishu), golden with a gradient from pale cream at the top to deep '
    'orange-gold at the bottom, a slight 3D bevel and a glossy highlight, a thick dark brown outline around every character.\n'
    'Decoration: none, or only a small simple ornament attached to the letters '
    '(for example a tiny star at the end of a stroke); nothing floating separately.\n'
    'Background: transparent background (PNG). No shadow, no glow, no sparkles, no frame, no scene behind the text.\n'
    'Landscape image, 1536x1024. The logo fills about 80% of the width, centered.')

# 地面材質 (spec 第 11 節):從正上方看、可以無縫拼接;一張蓋地圖 8×8 格。配色接近程式繪圖 (sprites.js 的 paintTile),
# 跟還是程式繪圖的地形交界才不會差太多
GROUND_ART = {
    'grass': ('short lush meadow grass made of many tiny grass blades, with a few very small lighter and darker patches',
              'medium grass green (about #4c9637), lighter green blade tips (about #67b64c), slightly darker green shading (about #43872f)'),
    'dark': ('shady forest floor grass made of many tiny dark grass blades, with a few tiny fallen leaves and small moss patches',
             'dark forest green (about #3a6630), lighter green blade tips (about #4f8443), darker shading (about #2e5226)'),
    'sand': ('a sandy dirt path surface: fine sand with many tiny pebbles',
             'warm sand beige (about #d2ad72), light tan grains (about #ddbd88), small darker brown pebbles (about #9c8058)'),
    'stone': ('village pavement made of rectangular stone slabs laid in staggered rows with thin grout lines, about 16 rows of slabs '
              'across the image; the rows must line up across the edges so the pattern continues',
              'warm light gray stone (about #a29e93) with lighter top edges (about #b9b5aa), darker gray grout lines (about #7d796f)'),
    'ash': ('scorched wasteland ground: dark cracked burnt earth covered with ash, with a few tiny orange-red embers',
            'dark brown-gray earth (about #4a3934), darker cracks (about #3b2c28), tiny orange-red embers (about #d0582a)'),
    'water': ('a calm lake water surface with soft gentle ripples only; keep it simple because the game animates the waves on top',
              'clear blue (about #2d6cc0), lighter blue ripple highlights (about #4a8ad8)'),
}


def ground_prompt(desc, colors):
    return ('Create a seamless tileable ground texture for the top-down 2D map of a 2000s Taiwanese MMORPG pet game.\n'
            'Ground: %s.\nColors: %s.\n'
            'View: seen straight from above (top-down), flat, no perspective, no horizon, no sky.\n'
            'Seamless: the texture must tile without visible seams: the left edge continues into the right edge, '
            'and the top edge continues into the bottom edge.\n'
            'Detail: the whole image covers 8 x 8 squares of the game map, so keep the details small and spread evenly over '
            'the whole image (many small details, not a few big ones). No single large feature (no big rock, no path, no puddle) '
            'that would make the repetition obvious. No cast shadows, even lighting across the whole image, no darker corners or vignette.\n'
            'Style: soft cel-shaded cartoon style that fits cute chibi game characters, but no dark outlines, and a little less '
            'saturated than the characters so they stand out on top of it.\n'
            'No text, no characters, no objects other than the small ground details described above.\nSquare image, 1024x1024.'
            % (desc, colors))


# 樹與裝飾 9 張 (spec 第 11 節):跟寵物一樣側面站著、腳底在正中央;影子由遊戲畫
DECO_ART = {
    'tree_plain1': ('a round leafy meadow tree with a short thick trunk and a big fluffy rounded crown made of a few leaf clusters',
                    'bright green leaves with light green highlights and dark green shading, warm brown trunk'),
    'tree_plain2': ('a smaller young meadow tree with a slightly lopsided oval crown of lighter leaves and a thin trunk',
                    'fresh light green leaves with yellow-green highlights and green shading, light brown trunk'),
    'tree_forest1': ('a tall pine tree made of three stacked triangular tiers of needles and a short trunk',
                     'dark green needles with blue-green highlights, dark brown trunk'),
    'tree_forest2': ('a slim spruce tree with drooping layered branches, taller and narrower than a pine',
                     'deep blue-green needles with lighter green tips, dark brown trunk'),
    'tree_dead': ('a dead leafless tree from a burnt wasteland: a twisted trunk and bare crooked branches',
                  'charcoal gray-brown bark with lighter gray highlights'),
    'rock1': ('a medium boulder with a few cracks and a small patch of moss on top',
              'gray stone with light gray highlights and darker gray shading, green moss'),
    'rock2': ('a small cluster of two or three rocks of different sizes, touching each other',
              'warm gray stone with light highlights and darker shading'),
    'bush': ('a low clump of tall wild grass blades growing from one spot',
             'grass green blades with light green tips and darker green at the base'),
    'flowers': ('a small low clump of wild flowers with green leaves, all growing from one spot',
                'red, yellow, white, pink-purple and blue flowers with yellow centers, green leaves'),
}


def deco_prompt(desc, colors):
    return ('If I attached a reference image, match its art style exactly (outline thickness, shading, colors), '
            'but draw the object described below.\n'
            'Create a game sprite of a map decoration for a 2000s Taiwanese MMORPG pet game, in the same cute chibi art style as the pets.\n'
            'Object: %s.\nColors: %s.\n%s\n'
            'View: side view from the front, standing upright (the game is a top-down 2D map where trees and rocks are drawn standing), '
            "the whole object visible, centered. The object's widest or tallest side fills about 70%% of the image.\n"
            'Background: transparent background (PNG). No shadow, no ground (the game draws the shadow), no text, '
            'no extra objects, only this one object.\nSquare image, 1024x1024.'
            % (desc, colors, STYLE))


# 代號跟遊戲對不上就直接失敗,不要產出檔名錯的 prompt
assert [o['cls'] for o in OWNERS] == list(G.CLASSES), '主人要跟 game_data.CLASSES 一致'
assert set(ITEM_ART) == set(G.ITEMS), '道具要跟 game_data.ITEMS 一致'
assert set(GROUND_ART) == set(G.ART_GROUND), '地面要跟 game_data.ART_GROUND 一致'
assert set(DECO_ART) == set(G.ART_DECO), '樹與裝飾要跟 game_data.ART_DECO 一致'


def category(title, intro):
    return ['---', '', '## ' + title, ''] + intro + ['']


lines = ['# 繪圖 prompt 集(ChatGPT 直接複製貼上)', '',
         '每一段都是完整的 prompt,不用拼湊。規格見 `美術規格.md` 與 `docs/phase-4/spec.md`。', '',
         '> 這份由 `docs/art/gen_prompts.py` 產生。要改 prompt 請改那支程式,再執行',
         '> `python3.8 docs/art/gen_prompts.py docs/art/繪圖prompt.md`(Windows 用 Python38 的完整路徑,見 `CLAUDE.md`)。', '',
         '## 怎麼用', '',
         '1. **產圖**:照下面的「產圖順序」找到要畫的圖,把 prompt 貼到 ChatGPT。每個類別的開頭寫了要不要開新對話、要上傳哪張參考圖。',
         '2. **存原圖**:下載後照箭頭後面的檔名存到 `art-src/`。一批畫完再一起處理,不用畫一張存一張。',
         '3. **請 Claude 先看一遍**:跟 Claude 說「圖放好了」。Claude 會照 spec 第 4.4 節逐張看原圖:角色被裁到(尾巴、耳朵、翅膀出框)、',
         '   身體朝左、灰白格子背景、一張圖裡有多隻、有文字或浮水印。有問題會列出檔名和原因,重畫或在工具裡處理(朝左就勾水平翻轉)。',
         '4. **批次存進遊戲**:開伺服器,用 Chrome、Edge 或 Firefox(Safari 不能存 WebP)打開 <http://localhost:8000/tools/sprite-tool.html>,',
         '   按上方的「批次」。工具會列出還沒處理的原圖,一次去背排成縮圖。看過縮圖後按「全部存進遊戲」。',
         '   標紅的那張會跳過並寫原因;要調容許值、筆刷、翻轉就點縮圖進單張模式,修好按「存進遊戲」。',
         '5. **看還缺哪些**:打開 <http://localhost:8000/tools/art-status.html>(美術進度表)。重新整理遊戲頁面就會看到新圖。',
         '6. 不滿意就直接用中文跟 GPT 說要改哪裡。常見的:',
         '   - 表情不夠兇 →「表情要更生氣,眉毛壓低成 V 字,不要笑」',
         '   - 顏色或造型跑掉 →「顏色和造型要跟第一張完全一樣,只改姿勢和表情」',
         '   - 角色畫太小 →「角色要跟第一張一樣大,最長邊約佔畫面 70%」',
         '7. GPT 偶爾會把灰白格子「畫」進圖裡(看起來透明其實不是),批次模式會把這張標紅。遇到時把 `Background:` 那一行換成',
         '   `Background: plain solid white background.`(白色系的用 `plain solid bright green background`),去背工具會處理。',
         '',
         '> 去背工具現在支援寵物、主人、NPC、道具四類。登入主視覺與 Logo(plan 第 10 項)、地面材質與樹與裝飾(第 13 項)還沒支援:',
         '> 原圖可以先放進 `art-src/`,批次模式會標紅寫「去背工具還沒支援」,等那一項做好再存。美術進度表照樣會算成「有原圖還沒處理」。',
         '',
         '## 產圖順序(spec 第 2 節)', '',
         '1. **第 1 批:野外與 BOSS 主圖 10 張**:綠史萊姆、哥布林、野狼、骷髏兵、月狐、彩虹鴿、吸血蝙蝠、獅鷲獸、幼龍、炎龍',
         '2. **主人 10 張**:先畫男騎士,當人物的畫風標準圖;定案後再畫其他 9 張',
         '3. **NPC 6 張**:要上傳男騎士和招牌寵物的成品圖,所以排在第 1 批和男騎士之後',
         '4. **第 2 批:進化線主圖 28 張**:一條進化線開一個對話',
         '5. **第 3 批:初階 13 種與炎龍的動作圖**(必要;噗噗、小火妖的 6 張已完成,還要 36 張)',
         '6. 中階、高階的動作圖可有可無,有空再補,沒有的用程式動畫',
         '',
         '道具、Logo、地面材質、樹與裝飾不依賴其他圖,隨時可以穿插。登入主視覺要等男騎士、女牧師、野狼、彩虹鴿都畫好。',
         '',
         '## 每段 prompt 在講什麼', '',
         '- **Colors**:寫死配色。重畫時顏色才不會跑掉(小火妖試做時,重畫的攻擊圖火焰顏色、角的形狀都變了)。',
         '- **大小**:主圖和動作圖都要求「最長邊約佔畫面 70%」,動作圖再要求「跟上一張一樣大」。有翅膀的寵物要求動作圖的翅膀張開程度不變(翅膀一收一放,工具自動對齊的大小就會跑掉)。',
         '- **Pose / Expression 分開寫**:攻擊身體往右前方衝、明講「不要笑」、眉毛壓成 V 字;受傷身體往左後倒、眼睛畫成 > <;'
         '睡著是往下彎的閉眼線。遊戲裡寵物只有 34~78px,表情要誇張才看得出來。',
         '- 動作圖明講「不要重新設計、不要加減特徵」,也不要求火焰變小、翅膀變大這種會改變大小的動作。',
         '- 會飛的寵物(小火妖、彩虹鴿、吸血蝙蝠)在遊戲裡是浮空的,睡著也畫成在空中打瞌睡。',
         '- **進化型態**(中階、高階):主圖要先上傳初階的圖當參考,prompt 會要求「看得出是同一系、更大更強」。'
         '動作圖的姿勢沿用初階。程式代號是初階加 2、3(例如 `poring2`),遊戲裡顯示大小是初階的 1.15 倍、1.3 倍。',
         '- **混種**(銀月狼、暮光鳥):只能配對得到,可以把爸媽兩張圖一起上傳當參考。',
         '- **人物**(主人、NPC):2.5 頭身,頭約佔身高 40%。遊戲裡主人只有 52px,頭約 20px,臉和髮型才看得清楚;頭像取上半身時是頭加胸口。',
         '  女主人跟男版同配色、同帽子武器,只換女版剪裁(例如騎士穿鎧甲短裙、獵人穿短褲)加長髮。',
         '  髮色每個職業一種、男女同色:騎士栗棕、獵人銅紅、牧師黑、法師銀紫、吟遊詩人金。',
         '- **主人的施法圖**:只畫動作,不畫光芒、光點、魔法陣、音符,光芒由程式畫;身體也不要前傾,前傾由程式做。只有用技能時會換成施法圖。',
         '- **NPC 的招牌寵物**:寵物一定要貼在 NPC 身上。分開畫的話,中間的背景去掉後寵物會飄在旁邊;'
         '寵物比最大一塊的 2% 還小時,還會被「清掉小碎塊」清掉。',
         '- **白色系**(白袍、白鬍子、白色寵物):米白色、沒有外框的部分容易被當成背景去掉,prompt 再要求一次外框;'
         'GPT 沒給透明背景就改用純綠背景。',
         '- **道具**:成品只有 64×64,遊戲裡顯示 32px,所以要求輪廓簡單、不能有字。',
         '- **地面材質**:從正上方看、上下左右可以無縫拼接、細節小而平均,不要大石頭或小路這種一眼看得出重複的東西;不要外框,角色站在上面才顯眼。',
         '- **樹與裝飾**:跟寵物一樣側面站著、腳底在正中央,影子由遊戲畫。',
         '',
         '> 階段 3(繁殖與進化)定案了全部 39 個種族:11 種 × 3 階 + 2 種混種 × 3 階。階段 4 照這份全面產圖。',
         '> 還沒有圖的種族,遊戲會用程式繪圖;進化型態沒有圖時,用初階的圖換顏色、放大。',
         '',
         '## 目錄', '',
         '- [寵物](#寵物):39 種加炎龍,主圖與動作圖',
         '- [主人](#主人):5 職業 × 男女 10 張',
         '- [NPC](#npc):6 張',
         '- [道具](#道具):16 張',
         '- [登入畫面](#登入畫面):主視覺、Logo',
         '- [地面材質](#地面材質):6 種,先試草地',
         '- [樹與裝飾](#樹與裝飾):9 張',
         '']

lines += category('寵物', [
    '1. **每隻寵物開一個新對話**。先把 `art-src/噗噗.png` 拖進對話當參考圖,再貼「主圖」。',
    '2. 主圖滿意後,**在同一個對話**依序貼「攻擊」「受傷」「睡著」。初階 13 種與炎龍的動作圖是必要的,中階、高階的可有可無。',
    '   對話不見了:先上傳那隻的主圖(`art-src/名字.png`)再貼動作圖。',
    '3. 動作圖會依主圖自動對齊大小:同一批有主圖就用同一批的,沒有就用遊戲裡的;兩邊都沒有,批次模式會標紅不存。',
    '   批次的縮圖看起來身體跟主圖不一樣大,就點縮圖進單張模式調「動作圖大小」。'])
for p in P + [BOSS]:
    for q in [p] + (forms_of(p) if p['code'] in EVO else []):
        lines += ['---', '', '### %s' % q['zh'], '']
        if q['note']:
            lines += [q['note'], '']
        name = q['zh'].split('(')[0]
        need = '可有可無' if q.get('stage') else '必要'   # 初階與炎龍的動作圖必要,中高階可有可無 (spec 第 1 節)
        lines.append(block('主圖(必要)', name + '.png', evo_prompt(q) if q.get('stage') else main_prompt(q)))
        for title, pose, face, allow in q['frames']:
            lines.append(block('%s(%s)' % (title, need), '%s_%s.png' % (name, title), frame_prompt(q, pose, face, allow)))

lines += category('主人', [
    '1. **男騎士排第一**,當所有人物(主人、NPC)的畫風標準圖。開新對話,先把 `art-src/噗噗.png` 拖進去,線條和上色才會跟寵物一致,再貼主圖。',
    '   男騎士定案、存進遊戲後,才畫其他 9 張。',
    '2. 其他男主人:每位開一個新對話,先上傳 `art-src/男騎士.png`,再貼主圖。',
    '3. 女主人:每位開一個新對話,先上傳 `art-src/男騎士.png`,再上傳同職業的男版圖(例如女獵人上傳 `art-src/男獵人.png`),再貼主圖。',
    '   女騎士只要上傳男騎士。所以女版要等同職業的男版畫好。',
    '4. 「施法」圖可有可無:主圖滿意後在同一個對話接著貼。不畫光芒、光點和音符,光芒由程式畫。',
    '   只有用技能時會換成施法圖;用道具、丟封印卡、換寵物只前傾。沒有施法圖時,用技能是主圖前傾加光芒。',
    '5. 只有男版圖、還沒有女版時,女角用程式繪圖(長髮),不會拿男版代替。'])
for o in OWNERS:
    for sex, sex_zh in (('m', '男'), ('f', '女')):
        name = sex_zh + G.CLASSES[o['cls']]['name']
        lines += ['---', '', '### ' + name, '']
        if o['cls'] == 'knight' and sex == 'm':
            note = '人物畫風標準圖,排第一。開新對話,先把 `art-src/噗噗.png` 拖進去,再貼主圖。定案、存進遊戲後才畫其他主人。'
        elif sex == 'm' or o['cls'] == 'knight':
            note = '開新對話,先上傳 `art-src/男騎士.png`,再貼主圖。'
        else:
            note = '開新對話,依序上傳 `art-src/男騎士.png`、`art-src/男%s.png`,再貼主圖。' % G.CLASSES[o['cls']]['name']
        if o.get('extra'):
            note += '\n\n白袍:' + GREEN_BG
        lines += [note, '']
        lines.append(block('主圖(必要)', name + '.png', owner_prompt(o, sex)))
        lines.append(block('施法(可有可無)', name + '_施法.png', owner_cast_prompt(o, sex)))

lines += category('NPC', [
    '1. **每位 NPC 開一個新對話**。先上傳男騎士的成品圖 `public/assets/owners/knight-m.webp`,再上傳招牌寵物的成品圖',
    '   (每段開頭有寫是哪一張),再貼 prompt。所以 NPC 要等男騎士和那隻寵物都存進遊戲才畫。',
    '2. 只畫一張站姿,呼吸、轉向玩家由程式做。名字和職務不變,改成奇幻種族混搭。',
    '3. **招牌寵物一定要貼在 NPC 身上**(坐在頭頂、趴在背包上、抱在懷裡)。寵物跟身體中間有空隙的話,去背後寵物會飄在旁邊,',
    '   太小的還會被「清掉小碎塊」清掉。',
    '   Claude 看原圖時也會檢查這一點。'])
for n in NPC_ART:
    pet = PET_BY_CODE[n['pet']]
    lines += ['---', '', '### ' + n['zh'], '']
    note = '依序上傳 `public/assets/owners/knight-m.webp`(男騎士)、`public/assets/pets/%s.webp`(%s),再貼 prompt。' % (pet['code'], pet['zh'])
    if n.get('white'):
        note += '\n\n白色系:' + GREEN_BG
    lines += [note, '']
    lines.append(block('站姿(必要)', n['zh'].split(' ')[-1] + '.png', npc_prompt(n)))

lines += category('道具', [
    '- 開一個新對話,先把 `art-src/噗噗.png` 拖進去當參考圖,畫風才跟寵物一樣,再一張一張貼。同一個對話接著畫,畫風比較一致。',
    '- 成品是 64×64、置中;背包和戰鬥道具欄顯示 32px,商店與說明視窗放大到 48px。沒有圖的道具維持程式繪圖。',
    '- 6 種蛋各長不一樣,看得出是哪種寵物的蛋。',
    '- 去背工具的「道具」類型會把圖裁到剛好、置中存成 64×64,批次模式也認得道具的原圖。'])
for code in G.ITEMS:
    zh = G.ITEMS[code]['name']
    if code == 'egg_dove':
        lines += ['白色的蛋:' + GREEN_BG, '']
    lines.append(block(zh, zh + '.png', item_prompt(*ITEM_ART[code])))

lines += category('登入畫面', [
    '- **主視覺**:要等男騎士、女牧師、野狼、彩虹鴿都畫好。開新對話,依序上傳 `art-src/男騎士.png`、`art-src/女牧師.png`、',
    '  `art-src/噗噗.png`、`art-src/小火妖.png`、`art-src/野狼.png`、`art-src/彩虹鴿.png`,再貼 prompt。',
    '  成品 1536×1024,鋪滿登入畫面的背景,中間放登入框;現在的天空動畫會改成疊在上面的飄動光點。',
    '- **Logo**:圖裡只畫「幻想之境」四個字,英文「FANTASIA ONLINE」維持網頁字,放在 Logo 圖下面。',
    '  中文字常畫錯,每張都要逐字看「幻、想、之、境」筆畫對不對;試很多次都畫不好,就維持現在的網頁字。',
    '- 去背工具還沒有「登入主視覺」「Logo」類型(plan 第 10 項),原圖先放進 `art-src/`。'])
lines.append(block('主視覺', G.ART_UI['login'] + '.png', LOGIN_PROMPT))
lines.append(block('Logo', G.ART_UI['logo'] + '.png', LOGO_PROMPT))

lines += category('地面材質', [
    '- **先試草地一種**。存進遊戲看效果,好看再畫其他 5 種;不好看就退回程式繪圖,其他 5 種不用畫(spec 第 11 節)。',
    '- 原圖 1024 會縮成 256×256,一張蓋地圖 8×8 格。工具會做無縫化(位移一半、融合接縫),也會顯示 3×3 拼起來的樣子看重複感。',
    '- 不用參考圖,每種開新對話直接貼。水面的水波動畫還是程式畫,材質只要平靜的水面。',
    '- 去背工具還沒有「地面材質」類型(plan 第 13 項),原圖先放進 `art-src/`。'])
for code, zh in G.ART_GROUND.items():
    title = zh.split('_')[-1] + ('(先試這張)' if code == 'grass' else '(草地好看才畫)')
    lines.append(block(title, zh + '.png', ground_prompt(*GROUND_ART[code])))

lines += category('樹與裝飾', [
    '- 開一個新對話,先把 `art-src/噗噗.png` 拖進去當參考圖,再一張一張貼。',
    '- 樹依區域換圖:艾爾文草原用草原樹,迷霧森林和狼嚎之丘用森林樹,亡者荒原用枯樹。岩石和草叢只是點綴,花叢畫在花地上。',
    '- 岩石、草叢、花叢要連成一塊:比最大一塊的 2% 還小的碎塊,去背時會被「清掉小碎塊」清掉。大小之後用比例對照頁定。',
    '- 去背工具還沒有「樹與裝飾」類型(plan 第 13 項),原圖先放進 `art-src/`。'])
for code, zh in G.ART_DECO.items():
    lines.append(block(zh, zh + '.png', deco_prompt(*DECO_ART[code])))

open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines).rstrip() + '\n')
print('ok', len(lines))
