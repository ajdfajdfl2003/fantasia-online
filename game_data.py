# -*- coding: utf-8 -*-
"""
幻想之境 Online — 遊戲數值資料

想調整平衡,改這個檔案就好,改完重開伺服器。
寵物素質、技能樹、孵蛋溫濕度參考自《寵物王 Online》(2003) 的攻略資料,見 docs/寵物王研究筆記.md
"""

# ============================================================
#  屬性相剋
# ============================================================
ELEMENTS = {'earth': '地', 'water': '水', 'wind': '風', 'fire': '火', 'light': '光', 'dark': '暗'}
ELEMENT_COLORS = {'earth': '#b08040', 'water': '#3a80e0', 'wind': '#50c080',
                  'fire': '#e85020', 'light': '#f0d040', 'dark': '#7040a0'}
# (攻擊方, 防守方):水剋火、火剋風、風剋地、地剋水,光暗互剋
STRONG = {('water', 'fire'), ('fire', 'wind'), ('wind', 'earth'), ('earth', 'water'),
          ('light', 'dark'), ('dark', 'light')}


def elem_mult(atk_el, def_el):
    if not atk_el or not def_el:
        return 1.0
    if (atk_el, def_el) in STRONG:
        return 1.3
    if (def_el, atk_el) in STRONG:
        return 0.75
    return 1.0


# 天氣 (法師可以改變):屬性 → 倍率
WEATHER = {
    'sun':  {'name': '烈日', 'fire': 1.3, 'light': 1.3, 'water': 0.8},
    'rain': {'name': '暴雨', 'water': 1.3, 'wind': 1.3, 'fire': 0.7},
}

FAMILIES = {'beast': '野獸屬', 'bug': '蟲獸屬', 'wing': '翼獸屬', 'humanoid': '類人屬', 'fairy': '妖精屬'}

# ============================================================
#  寵物技能
#  type: phys 物理 / mag 魔法 / status 狀態 / heal 治療
#  target: enemy 單一敵人 / enemies 全體敵人 / ally 單一隊友
# ============================================================
PET_SKILLS = {
    'tackle':     {'name': '撞擊', 'mp': 3, 'type': 'phys', 'mult': 1.4, 'target': 'enemy', 'fx': 'slam'},
    'double':     {'name': '二段攻擊', 'mp': 5, 'type': 'phys', 'mult': 0.8, 'hits': 2, 'target': 'enemy', 'fx': 'slash'},
    'triple':     {'name': '三段攻擊', 'mp': 9, 'type': 'phys', 'mult': 0.75, 'hits': 3, 'target': 'enemy', 'fx': 'slash'},
    'sneak':      {'name': '偷襲', 'mp': 6, 'type': 'phys', 'mult': 1.3, 'pierce': True, 'target': 'enemy', 'fx': 'slash',
                   'desc': '無視對方防禦'},
    'poison':     {'name': '毒擊', 'mp': 6, 'type': 'phys', 'mult': 0.9, 'status': ('poison', 10), 'target': 'enemy', 'fx': 'poison'},
    'drain':      {'name': '吸血', 'mp': 6, 'type': 'phys', 'mult': 1.1, 'el': 'dark', 'drain': 0.5, 'target': 'enemy', 'fx': 'drain',
                   'desc': '吸收造成傷害的一半'},
    'rock':       {'name': '落石', 'mp': 6, 'type': 'mag', 'el': 'earth', 'mult': 1.6, 'target': 'enemy', 'fx': 'rock'},
    'quake':      {'name': '地震', 'mp': 14, 'type': 'mag', 'el': 'earth', 'mult': 1.1, 'target': 'enemies', 'fx': 'quake'},
    'fireball':   {'name': '火球', 'mp': 6, 'type': 'mag', 'el': 'fire', 'mult': 1.6, 'target': 'enemy', 'fx': 'fire'},
    'flamerain':  {'name': '焰星雨', 'mp': 14, 'type': 'mag', 'el': 'fire', 'mult': 1.1, 'target': 'enemies', 'fx': 'flamerain'},
    'iceball':    {'name': '冰球', 'mp': 6, 'type': 'mag', 'el': 'water', 'mult': 1.6, 'target': 'enemy', 'fx': 'ice'},
    'icicle':     {'name': '冰柱', 'mp': 14, 'type': 'mag', 'el': 'water', 'mult': 1.1, 'target': 'enemies', 'fx': 'icicle'},
    'gale':       {'name': '狂風', 'mp': 6, 'type': 'mag', 'el': 'wind', 'mult': 1.6, 'target': 'enemy', 'fx': 'wind'},
    'storm':      {'name': '風暴', 'mp': 14, 'type': 'mag', 'el': 'wind', 'mult': 1.1, 'target': 'enemies', 'fx': 'storm'},
    'laser':      {'name': '雷射', 'mp': 7, 'type': 'mag', 'el': 'light', 'mult': 1.7, 'target': 'enemy', 'fx': 'laser'},
    'holy':       {'name': '聖光陣', 'mp': 14, 'type': 'mag', 'el': 'light', 'mult': 1.1, 'target': 'enemies', 'fx': 'holy'},
    'darkcircle': {'name': '暗法陣', 'mp': 14, 'type': 'mag', 'el': 'dark', 'mult': 1.1, 'target': 'enemies', 'fx': 'darkc'},
    'sleep':      {'name': '睡眠', 'mp': 8, 'type': 'status', 'status': ('sleep', 6), 'chance': 0.6, 'target': 'enemy', 'fx': 'sleep',
                   'desc': '60% 機率讓敵人睡著 6 秒 (被打會醒)'},
    'weaken':     {'name': '防禦弱化', 'mp': 6, 'type': 'status', 'status': ('defdown', 15), 'chance': 1.0, 'target': 'enemy',
                   'fx': 'debuff', 'desc': '敵人防禦力下降 30%,持續 15 秒'},
    'heal':       {'name': '治療', 'mp': 8, 'type': 'heal', 'mult': 0.3, 'target': 'ally', 'fx': 'heal',
                   'desc': '恢復隊友 30% HP'},
    'breath':     {'name': '龍息', 'mp': 16, 'type': 'mag', 'el': 'fire', 'mult': 1.4, 'target': 'enemies', 'fx': 'breath'},
    'bite':       {'name': '撕咬', 'mp': 5, 'type': 'phys', 'mult': 1.7, 'status': ('defdown', 10), 'chance': 0.4, 'target': 'enemy',
                   'fx': 'bite', 'desc': '40% 讓敵人防禦力下降 30%,持續 10 秒'},

    # ----- 中階 / 高階 (進化時種族技能線升階,見 SKILL_TIERS) -----
    'strike':     {'name': '強力撞擊', 'mp': 5, 'type': 'phys', 'mult': 1.8, 'target': 'enemy', 'fx': 'slam'},
    'smash':      {'name': '超強撞擊', 'mp': 8, 'type': 'phys', 'mult': 2.3, 'target': 'enemy', 'fx': 'slam'},
    'quad':       {'name': '四段攻擊', 'mp': 13, 'type': 'phys', 'mult': 0.7, 'hits': 4, 'target': 'enemy', 'fx': 'slash'},
    'assassin':   {'name': '暗殺', 'mp': 9, 'type': 'phys', 'mult': 1.7, 'pierce': True, 'target': 'enemy', 'fx': 'slash',
                   'desc': '無視對方防禦'},
    'assassin2':  {'name': '強力暗殺', 'mp': 13, 'type': 'phys', 'mult': 2.2, 'pierce': True, 'target': 'enemy', 'fx': 'slash',
                   'desc': '無視對方防禦'},
    'bite2':      {'name': '猛咬', 'mp': 8, 'type': 'phys', 'mult': 2.1, 'status': ('defdown', 10), 'chance': 0.4, 'target': 'enemy',
                   'fx': 'bite', 'desc': '40% 讓敵人防禦力下降 30%,持續 10 秒'},
    'bite3':      {'name': '致命咬', 'mp': 12, 'type': 'phys', 'mult': 2.6, 'status': ('defdown', 12), 'chance': 0.4, 'target': 'enemy',
                   'fx': 'bite', 'desc': '40% 讓敵人防禦力下降 30%,持續 12 秒'},
    'absorb':     {'name': '能量吸收', 'mp': 9, 'type': 'phys', 'mult': 1.4, 'el': 'dark', 'drain': 0.55, 'target': 'enemy', 'fx': 'drain',
                   'desc': '吸收造成傷害的 55%'},
    'lifesteal':  {'name': '生命掠奪', 'mp': 13, 'type': 'phys', 'mult': 1.8, 'el': 'dark', 'drain': 0.6, 'target': 'enemy', 'fx': 'drain',
                   'desc': '吸收造成傷害的 60%'},
    'fireball2':  {'name': '大火球', 'mp': 9, 'type': 'mag', 'el': 'fire', 'mult': 2.0, 'target': 'enemy', 'fx': 'fire'},
    'fireball3':  {'name': '爆炎球', 'mp': 13, 'type': 'mag', 'el': 'fire', 'mult': 2.5, 'target': 'enemy', 'fx': 'fire'},
    'iceball2':   {'name': '大冰球', 'mp': 9, 'type': 'mag', 'el': 'water', 'mult': 2.0, 'target': 'enemy', 'fx': 'ice'},
    'iceball3':   {'name': '冰晶彈', 'mp': 13, 'type': 'mag', 'el': 'water', 'mult': 2.5, 'target': 'enemy', 'fx': 'ice'},
    'gale2':      {'name': '颶風', 'mp': 9, 'type': 'mag', 'el': 'wind', 'mult': 2.0, 'target': 'enemy', 'fx': 'wind'},
    'gale3':      {'name': '真空刃', 'mp': 13, 'type': 'mag', 'el': 'wind', 'mult': 2.5, 'target': 'enemy', 'fx': 'wind'},
    'laser2':     {'name': '強力雷射', 'mp': 10, 'type': 'mag', 'el': 'light', 'mult': 2.1, 'target': 'enemy', 'fx': 'laser'},
    'laser3':     {'name': '極光射線', 'mp': 14, 'type': 'mag', 'el': 'light', 'mult': 2.6, 'target': 'enemy', 'fx': 'laser'},
    'quake2':     {'name': '大地震', 'mp': 19, 'type': 'mag', 'el': 'earth', 'mult': 1.35, 'target': 'enemies', 'fx': 'quake'},
    'quake3':     {'name': '地裂', 'mp': 26, 'type': 'mag', 'el': 'earth', 'mult': 1.65, 'target': 'enemies', 'fx': 'quake'},
    'flamerain2': {'name': '流星火雨', 'mp': 19, 'type': 'mag', 'el': 'fire', 'mult': 1.35, 'target': 'enemies', 'fx': 'flamerain'},
    'flamerain3': {'name': '隕石雨', 'mp': 26, 'type': 'mag', 'el': 'fire', 'mult': 1.65, 'target': 'enemies', 'fx': 'flamerain'},
    'icicle2':    {'name': '冰風暴', 'mp': 19, 'type': 'mag', 'el': 'water', 'mult': 1.35, 'target': 'enemies', 'fx': 'icicle'},
    'icicle3':    {'name': '絕對零度', 'mp': 26, 'type': 'mag', 'el': 'water', 'mult': 1.65, 'target': 'enemies', 'fx': 'icicle'},
    'holy2':      {'name': '神聖光陣', 'mp': 19, 'type': 'mag', 'el': 'light', 'mult': 1.35, 'target': 'enemies', 'fx': 'holy'},
    'holy3':      {'name': '超聖光陣', 'mp': 26, 'type': 'mag', 'el': 'light', 'mult': 1.65, 'target': 'enemies', 'fx': 'holy'},
    'darkcircle2': {'name': '深淵法陣', 'mp': 19, 'type': 'mag', 'el': 'dark', 'mult': 1.35, 'target': 'enemies', 'fx': 'darkc'},
    'darkcircle3': {'name': '冥界法陣', 'mp': 26, 'type': 'mag', 'el': 'dark', 'mult': 1.65, 'target': 'enemies', 'fx': 'darkc'},
    'breath2':    {'name': '烈焰龍息', 'mp': 22, 'type': 'mag', 'el': 'fire', 'mult': 1.7, 'target': 'enemies', 'fx': 'breath'},
    'breath3':    {'name': '煉獄龍息', 'mp': 30, 'type': 'mag', 'el': 'fire', 'mult': 2.0, 'target': 'enemies', 'fx': 'breath'},
    'sleep2':     {'name': '中階睡眠', 'mp': 10, 'type': 'status', 'status': ('sleep', 8), 'chance': 0.75, 'target': 'enemy', 'fx': 'sleep',
                   'desc': '75% 機率讓敵人睡著 8 秒 (被打會醒)'},
    'sleep3':     {'name': '高階睡眠', 'mp': 12, 'type': 'status', 'status': ('sleep', 10), 'chance': 0.9, 'target': 'enemy', 'fx': 'sleep',
                   'desc': '90% 機率讓敵人睡著 10 秒 (被打會醒)'},
    'weaken2':    {'name': '持久弱化', 'mp': 8, 'type': 'status', 'status': ('defdown', 25), 'chance': 1.0, 'target': 'enemy',
                   'fx': 'debuff', 'desc': '敵人防禦力下降 30%,持續 25 秒'},
    'weaken3':    {'name': '全體弱化', 'mp': 14, 'type': 'status', 'status': ('defdown', 20), 'chance': 1.0, 'target': 'enemies',
                   'fx': 'debuff', 'desc': '全體敵人防禦力下降 30%,持續 20 秒'},
    'heal2':      {'name': '強力治療', 'mp': 11, 'type': 'heal', 'mult': 0.45, 'target': 'ally', 'fx': 'heal',
                   'desc': '恢復隊友 45% HP'},
    'heal3':      {'name': '群體治療術', 'mp': 16, 'type': 'heal', 'mult': 0.3, 'target': 'allies', 'fx': 'heal',
                   'desc': '我方全體寵物恢復 30% HP'},

    # ----- 專屬技能 (中階學會,不能遺傳,見 EXCLUSIVE) -----
    'jellyeat':   {'name': '果凍吞噬', 'mp': 8, 'type': 'phys', 'el': 'earth', 'mult': 1.5, 'drain': 0.5, 'target': 'enemy',
                   'fx': 'slam', 'desc': '吸收造成傷害的 50%'},
    'acid':       {'name': '強酸黏液', 'mp': 8, 'type': 'phys', 'el': 'water', 'mult': 1.2, 'status': ('defdown', 15), 'target': 'enemy',
                   'fx': 'poison', 'desc': '60% 讓敵人防禦力下降 30%,持續 15 秒'},
    'pilfer':     {'name': '順手牽羊', 'mp': 6, 'type': 'phys', 'mult': 1.2, 'steal': 3, 'target': 'enemy', 'fx': 'slash',
                   'desc': '打中時偷到金幣 (敵人等級 ×3),每隻敵人只能偷一次'},
    'howl':       {'name': '狼嚎', 'mp': 10, 'type': 'status', 'status': ('atkup', 15), 'chance': 1.0, 'target': 'allies', 'fx': 'roar',
                   'desc': '我方全體寵物攻擊力提升 30%,持續 15 秒'},
    'curse':      {'name': '亡者詛咒', 'mp': 12, 'type': 'status', 'status': ('atkdown', 12), 'chance': 0.8, 'target': 'enemies',
                   'fx': 'debuff', 'desc': '80% 讓全體敵人攻擊力下降 20%,持續 12 秒'},
    'firedance':  {'name': '火妖之舞', 'mp': 18, 'type': 'mag', 'el': 'fire', 'mult': 1.3, 'status': ('poison', 10), 'chance': 0.4,
                   'target': 'enemies', 'fx': 'flamerain', 'desc': '全體火屬性魔法,各 40% 灼傷 (持續扣血)'},
    'blessing':   {'name': '七彩祝福', 'mp': 14, 'type': 'heal', 'mult': 0.25, 'target': 'allies', 'fx': 'heal',
                   'desc': '我方全體寵物恢復 25% HP'},
    'moonshade':  {'name': '幻月', 'mp': 10, 'type': 'mag', 'el': 'water', 'mult': 1.5, 'status': ('sleep', 6), 'target': 'enemy',
                   'fx': 'ice', 'desc': '60% 讓敵人睡著 6 秒'},
    'feast':      {'name': '血之盛宴', 'mp': 16, 'type': 'phys', 'el': 'dark', 'mult': 0.8, 'drain': 0.4, 'target': 'enemies',
                   'fx': 'darkc', 'desc': '全體攻擊,吸收造成傷害的 40%'},
    'dive':       {'name': '天空俯衝', 'mp': 12, 'type': 'phys', 'el': 'light', 'mult': 2.2, 'pierce': True, 'target': 'enemy',
                   'fx': 'slam', 'desc': '無視對方防禦'},
    'dragonrage': {'name': '龍之怒', 'mp': 18, 'type': 'mag', 'el': 'fire', 'mult': 2.6, 'target': 'enemy', 'fx': 'fire'},
    'moonfang':   {'name': '月下狼牙', 'mp': 10, 'type': 'phys', 'el': 'water', 'mult': 0.75, 'hits': 3, 'target': 'enemy', 'fx': 'slash'},
    'duskveil':   {'name': '暮光幻影', 'mp': 16, 'type': 'status', 'status': ('sleep', 6), 'chance': 0.5, 'target': 'enemies',
                   'fx': 'darkc', 'desc': '50% 讓全體敵人睡著 6 秒 (被打會醒)'},
}

# 種族技能線:初階 → 中階 → 高階 (進化時升階;遺傳也是以初階代號記錄)
SKILL_TIERS = {
    'tackle': ('tackle', 'strike', 'smash'), 'double': ('double', 'triple', 'quad'),
    'sneak': ('sneak', 'assassin', 'assassin2'), 'bite': ('bite', 'bite2', 'bite3'),
    'drain': ('drain', 'absorb', 'lifesteal'), 'fireball': ('fireball', 'fireball2', 'fireball3'),
    'iceball': ('iceball', 'iceball2', 'iceball3'), 'gale': ('gale', 'gale2', 'gale3'),
    'laser': ('laser', 'laser2', 'laser3'), 'quake': ('quake', 'quake2', 'quake3'),
    'flamerain': ('flamerain', 'flamerain2', 'flamerain3'), 'icicle': ('icicle', 'icicle2', 'icicle3'),
    'holy': ('holy', 'holy2', 'holy3'), 'darkcircle': ('darkcircle', 'darkcircle2', 'darkcircle3'),
    'breath': ('breath', 'breath2', 'breath3'), 'sleep': ('sleep', 'sleep2', 'sleep3'),
    'weaken': ('weaken', 'weaken2', 'weaken3'), 'heal': ('heal', 'heal2', 'heal3'),
}
# 專屬技能 (種族系 → 技能):中階學會,不能遺傳
EXCLUSIVE = {
    'poring': 'jellyeat', 'slime': 'acid', 'goblin': 'pilfer', 'wolf': 'howl', 'skeleton': 'curse', 'imp': 'firedance',
    'dove': 'blessing', 'fox': 'moonshade', 'bat': 'feast', 'griffin': 'dive', 'drake': 'dragonrage',
    'silverwolf': 'moonfang', 'duskbird': 'duskveil',
}

# ============================================================
#  寵物種族
#  base: 初始 (力量, 體質, 智力, 敏捷)    grow: 每升一級得到的自由點數
#  pref: 自動配點 / 天生素質的偏好權重      skills: (技能, 學會等級)
#  cap: 捕捉難易度 (越高越好抓,0 = 無法捕捉)
#  egg: 有蛋的寵物 (商店價格、最佳孵化溫度與濕度)
#  love / hate: 最愛 / 討厭的食物 (love = '*' 表示雜食,每種都喜歡)
#  trick: 表演 (名稱, 動作, 喊的話)  動作:bounce squash spin howl shake fire circle flip jump
# ============================================================
SPECIES = {
    'poring':   {'name': '噗噗', 'el': 'earth', 'fam': 'bug', 'base': (15, 14, 9, 12), 'grow': 4, 'pref': (1, 2, 1, 1),
                 'skills': [('tackle', 1), ('heal', 5), ('quake', 10)], 'cap': 0.75, 'hatch': (50, 70),
                 'love': 'berry', 'hate': 'wood', 'trick': ('彈跳三連', 'bounce', '噗噗噗!')},
    'slime':    {'name': '綠史萊姆', 'el': 'water', 'fam': 'bug', 'base': (16, 10, 10, 12), 'grow': 5, 'pref': (2, 1, 1, 1),
                 'skills': [('double', 1), ('iceball', 5), ('sneak', 10)], 'cap': 0.7, 'hatch': (40, 90),
                 'love': '*', 'hate': None, 'trick': ('軟Q壓扁', 'squash', '啵~')},
    'goblin':   {'name': '哥布林', 'el': 'earth', 'fam': 'humanoid', 'base': (14, 14, 8, 12), 'grow': 4, 'pref': (2, 2, 0, 1),
                 'skills': [('tackle', 1), ('sneak', 5), ('heal', 10)], 'cap': 0.6, 'hatch': (70, 40),
                 'love': 'wheat', 'hate': 'fish', 'trick': ('揮棒轉圈', 'spin', '嘿嘿!')},
    'wolf':     {'name': '野狼', 'el': 'wind', 'fam': 'beast', 'base': (18, 13, 8, 17), 'grow': 4, 'pref': (2, 1, 0, 2),
                 'skills': [('double', 1), ('gale', 5), ('bite', 10)], 'cap': 0.55, 'hatch': (55, 45),
                 'love': 'meat', 'hate': 'wheat', 'trick': ('仰天長嚎', 'howl', '嗷嗚~')},
    'skeleton': {'name': '骷髏兵', 'el': 'dark', 'fam': 'humanoid', 'base': (20, 10, 16, 15), 'grow': 5, 'pref': (2, 1, 1, 1),
                 'skills': [('double', 1), ('darkcircle', 5), ('drain', 10)], 'cap': 0.45, 'hatch': (80, 30),
                 'love': 'wood', 'hate': 'meat', 'trick': ('骨頭喀啦喀啦', 'shake', '喀啦喀啦')},
    'imp':      {'name': '小火妖', 'el': 'fire', 'fam': 'fairy', 'base': (12, 12, 22, 16), 'grow': 6, 'pref': (0, 1, 3, 1),
                 'skills': [('fireball', 1), ('weaken', 5), ('flamerain', 10)], 'cap': 0.4,
                 'egg': {'price': 450, 'temp': 90, 'hum': 10},
                 'love': 'ore', 'hate': 'fish', 'trick': ('噴火圈', 'fire', '呼~!')},
    'dove':     {'name': '彩虹鴿', 'el': 'light', 'fam': 'wing', 'base': (22, 18, 15, 18), 'grow': 4, 'pref': (2, 1, 1, 1),
                 'skills': [('double', 1), ('laser', 5), ('heal', 10)], 'cap': 0.5,
                 'egg': {'price': 260, 'temp': 60, 'hum': 35},
                 'love': 'wheat', 'hate': 'meat', 'trick': ('繞圈飛', 'circle', '咕咕~')},
    'fox':      {'name': '月狐', 'el': 'water', 'fam': 'beast', 'base': (16, 10, 19, 16), 'grow': 4, 'pref': (0, 1, 2, 1),
                 'skills': [('iceball', 1), ('sleep', 5), ('icicle', 10)], 'cap': 0.45,
                 'egg': {'price': 260, 'temp': 50, 'hum': 60},
                 'love': 'fish', 'hate': 'wood', 'trick': ('追尾巴', 'spin', '嗚嗚~')},
    'bat':      {'name': '吸血蝙蝠', 'el': 'dark', 'fam': 'wing', 'base': (19, 18, 18, 18), 'grow': 5, 'pref': (1, 1, 1, 1),
                 'skills': [('drain', 1), ('sleep', 5), ('darkcircle', 10)], 'cap': 0.45,
                 'egg': {'price': 320, 'temp': 60, 'hum': 60},
                 'love': 'berry', 'hate': 'wheat', 'trick': ('倒吊', 'flip', '吱吱!')},
    'griffin':  {'name': '獅鷲獸', 'el': 'light', 'fam': 'wing', 'base': (20, 20, 13, 20), 'grow': 5, 'pref': (2, 1, 1, 2),
                 'skills': [('tackle', 1), ('holy', 5), ('weaken', 10)], 'cap': 0.3,
                 'egg': {'price': 900, 'temp': 60, 'hum': 60},
                 'love': 'meat', 'hate': 'berry', 'trick': ('展翅高飛', 'jump', '嘎——!')},
    'drake':    {'name': '幼龍', 'el': 'fire', 'fam': 'wing', 'base': (22, 20, 20, 18), 'grow': 6, 'pref': (1, 1, 1, 1),
                 'skills': [('tackle', 1), ('fireball', 3), ('breath', 8)], 'cap': 0,
                 'egg': {'price': 3000, 'temp': 95, 'hum': 20, 'shop': False},
                 'love': 'ore', 'hate': 'fish', 'trick': ('噴小火苗', 'fire', '噗~呼!')},
    # ----- 混種 (只能靠配對得到,見 HYBRIDS) -----
    'silverwolf': {'name': '銀月狼', 'el': 'water', 'fam': 'beast', 'base': (19, 12, 16, 18), 'grow': 5, 'pref': (2, 1, 1, 2),
                   'skills': [('bite', 1), ('iceball', 5), ('sleep', 10)], 'cap': 0, 'hatch': (50, 55), 'hybrid': True,
                   'love': 'meat', 'hate': 'wood', 'trick': ('對月長嚎', 'howl', '嗷嗚——')},
    'duskbird':   {'name': '暮光鳥', 'el': 'dark', 'fam': 'wing', 'base': (19, 17, 18, 20), 'grow': 5, 'pref': (1, 1, 1, 1),
                   'skills': [('drain', 1), ('laser', 5), ('heal', 10)], 'cap': 0, 'hatch': (60, 45), 'hybrid': True,
                   'love': 'berry', 'hate': 'meat', 'trick': ('夜空翱翔', 'circle', '咕吱~')},
}

# 混種:兩個種族系配對時多一個選項 (不分順序、任何階段都算)
HYBRIDS = {
    frozenset(('wolf', 'fox')): 'silverwolf',
    frozenset(('dove', 'bat')): 'duskbird',
}

# 進化型態:種族系 → ((中階名字, 程式繪圖的濾鏡), (高階名字, 濾鏡))
# 程式代號是初階代號加 2、3 (poring2、poring3);沒有專屬圖片時,用初階的樣子套濾鏡、放大
FORMS = {
    'poring':     (('彈彈噗', 'hue-rotate(-45deg) saturate(1.2)'), ('噗噗國王', 'hue-rotate(55deg) saturate(1.5)')),
    'slime':      (('大史萊姆', 'hue-rotate(60deg)'), ('史萊姆王', 'hue-rotate(150deg) saturate(1.3)')),
    'goblin':     (('哥布林戰士', 'hue-rotate(-30deg) saturate(1.2)'), ('哥布林酋長', 'hue-rotate(-90deg) saturate(1.3)')),
    'wolf':       (('疾風狼', 'sepia(0.6) hue-rotate(60deg) saturate(1.5)'), ('狼王', 'brightness(0.55) contrast(1.3)')),
    'skeleton':   (('骷髏騎士', 'sepia(0.5) hue-rotate(180deg) saturate(1.3)'), ('骷髏將軍', 'sepia(0.8) hue-rotate(-20deg) saturate(2)')),
    'imp':        (('火妖', 'hue-rotate(-25deg) saturate(1.3)'), ('炎魔', 'hue-rotate(200deg) saturate(1.4)')),
    'dove':       (('虹光鴿', 'sepia(0.4) saturate(2) hue-rotate(10deg)'), ('天虹鳥', 'sepia(0.6) saturate(3) hue-rotate(-10deg)')),
    'fox':        (('雪月狐', 'hue-rotate(20deg) saturate(1.5)'), ('九尾月狐', 'sepia(0.5) saturate(2) hue-rotate(-15deg)')),
    'bat':        (('血翼蝠', 'hue-rotate(60deg) saturate(1.6)'), ('夜王蝠', 'brightness(0.6) saturate(1.4)')),
    'griffin':    (('獅鷲騎獸', 'hue-rotate(180deg) saturate(1.1)'), ('皇家獅鷲', 'hue-rotate(-15deg) saturate(1.8)')),
    'drake':      (('飛龍', 'hue-rotate(-20deg) saturate(1.2)'), ('赤炎龍', 'hue-rotate(-35deg) saturate(1.5)')),
    'silverwolf': (('月影狼', 'hue-rotate(40deg) saturate(1.3)'), ('天狼', 'brightness(1.15) saturate(0.6)')),
    'duskbird':   (('夜虹鳥', 'hue-rotate(40deg) saturate(1.3)'), ('晨昏鳳凰', 'hue-rotate(-60deg) saturate(1.6)')),
}
# 進化:條件 (中階, 高階)、能力倍率、每級多給的點數、賣價加成、顯示大小倍率
EVOLVE = {'lv': (12, 24), 'bond': (40, 70), 'stat': (1.25, 1.5), 'grow': (1, 2), 'price': (150, 400), 'scale': (1.15, 1.3)}


def _make_forms():
    """從初階產生中階、高階的種族資料 (poring → poring2、poring3)"""
    for line in list(SPECIES):
        sp = SPECIES[line]
        sp.update({'line': line, 'stage': 0, 'evo': line + '2'})
        for st in (1, 2):
            name, look = FORMS[line][st - 1]
            k = EVOLVE['stat'][st - 1]
            SPECIES[line + str(st + 1)] = {
                'name': name, 'el': sp['el'], 'fam': sp['fam'], 'base': tuple(int(round(v * k)) for v in sp['base']),
                'grow': sp['grow'] + EVOLVE['grow'][st - 1], 'pref': sp['pref'],
                'skills': [(SKILL_TIERS[s][st], lv) for s, lv in sp['skills']] + [(EXCLUSIVE[line], 1)],
                'cap': 0, 'love': sp['love'], 'hate': sp['hate'], 'trick': sp['trick'],
                'line': line, 'stage': st, 'evo': line + '3' if st == 1 else None,
                'look': {'from': line, 'filter': look, 'scale': EVOLVE['scale'][st - 1], 'shine': st == 2},
            }


_make_forms()


def hatch_pref(sp):
    """這個種族的蛋喜歡的 (溫度, 濕度)"""
    s = SPECIES[sp]
    return (s['egg']['temp'], s['egg']['hum']) if 'egg' in s else s['hatch']


def pet_skills(sp, lv, inh=None):
    """會的技能:種族技能 (依等級) + 專屬技能 (中階以上) + 遺傳技能 (跟著階段升階)"""
    s = SPECIES[sp]
    out = [k for k, need in s['skills'] if lv >= need]
    if inh in SKILL_TIERS:
        k = SKILL_TIERS[inh][s.get('stage', 0)]
        if k not in out:
            out.append(k)
    return out


def inheritable(sp, inh=None):
    """這隻寵物可以遺傳給小寵的技能 (初階代號):種族技能線 + 自己的遺傳技能,不含專屬技能"""
    out = [k for k, _ in SPECIES[SPECIES[sp]['line']]['skills']]
    if inh in SKILL_TIERS and inh not in out:
        out.append(inh)
    return out


def derive(lv, st):
    """由 (力, 體, 智, 敏) 算出戰鬥數值 — 公式參考寵物王:1 體質 = 4 HP、1 智力 = 3 MP"""
    s, v, i, a = st
    return {'mhp': 30 + v * 4 + lv * 5, 'mmp': 10 + i * 3,
            'atk': int(s * 1.5 + lv), 'matk': int(i * 1.4 + lv),
            'def': int(v * 0.5 + lv * 0.5), 'mdef': int(i * 0.4 + v * 0.2 + lv * 0.5),
            'spd': 18 + a * 0.8, 'eva': min(0.25, 0.03 + a * 0.0015)}


def exp_need(lv):
    return int(10 + 12 * lv ** 1.7)


def stars(q):
    """天生素質點 (0~12) → 星等"""
    return 5 if q >= 12 else 4 if q >= 9 else 3 if q >= 6 else 2 if q >= 3 else 1


# 野生寵物的天生素質分布 (0~12 點的權重):大多普通,12 點極品非常稀有
WILD_QUALITY_WEIGHTS = [8, 10, 12, 12, 11, 10, 8, 6, 4, 3, 2, 1, 0.4]
WILD_POWER = 0.72          # 野生怪的 HP 與攻擊力倍率 (比玩家養的寵物弱一點)

# ============================================================
#  主人職業 (原作 5 職業) — 主人不能攻擊,只能輔助
#  eff 種類:buff / debuff / heal / shield / revive / bar / weather / mpall / sleep / hasteall
# ============================================================
CLASSES = {
    'knight': {'name': '騎士', 'hp': 120, 'mp': 30, 'ghp': 15, 'gmp': 4, 'spd': 20,
               'enc': 1.0, 'cap': 1.0, 'flee': 0.7, 'desc': '強化寵物攻防,削弱敵人',
               'skills': [
                   {'name': '鼓舞', 'mp': 8, 'lv': 1, 'target': 'ally', 'eff': 'buff', 'st': 'atkup', 'dur': 15,
                    'desc': '我方寵物攻擊力提升 30%,持續 15 秒'},
                   {'name': '守護', 'mp': 8, 'lv': 3, 'target': 'ally', 'eff': 'buff', 'st': 'defup', 'dur': 15,
                    'desc': '我方寵物防禦力提升 40%,持續 15 秒'},
                   {'name': '威嚇', 'mp': 15, 'lv': 6, 'target': 'enemies', 'eff': 'debuff', 'st': 'atkdown', 'dur': 12,
                    'desc': '全體敵人攻擊力下降 20%,持續 12 秒'}]},
    'hunter': {'name': '獵人', 'hp': 100, 'mp': 35, 'ghp': 12, 'gmp': 5, 'spd': 20,
               'enc': 0.7, 'cap': 1.35, 'flee': 0.9, 'desc': '操控時間棒,捕捉成功率高,遇敵率低',
               'skills': [
                   {'name': '疾風', 'mp': 6, 'lv': 1, 'target': 'ally', 'eff': 'bar', 'val': 50,
                    'desc': '我方寵物的時間棒立刻增加 50%'},
                   {'name': '遲緩', 'mp': 8, 'lv': 3, 'target': 'enemy', 'eff': 'debuff', 'st': 'slow', 'dur': 10, 'val': -50,
                    'desc': '敵人時間棒減少 50%,並變慢 10 秒'},
                   {'name': '看破', 'mp': 10, 'lv': 6, 'target': 'enemy', 'eff': 'debuff', 'st': 'defdown', 'dur': 15,
                    'desc': '敵人防禦力下降 30%,持續 15 秒'}]},
    'priest': {'name': '牧師', 'hp': 95, 'mp': 50, 'ghp': 11, 'gmp': 7, 'spd': 20,
               'enc': 1.1, 'cap': 1.0, 'flee': 0.7, 'desc': '治療寵物、防護罩、復活',
               'skills': [
                   {'name': '治癒術', 'mp': 8, 'lv': 1, 'target': 'ally', 'eff': 'heal', 'val': 0.35,
                    'desc': '恢復我方寵物 35% HP'},
                   {'name': '防護罩', 'mp': 10, 'lv': 3, 'target': 'ally', 'eff': 'shield', 'val': 0.3,
                    'desc': '替寵物張開可吸收 30% 最大 HP 傷害的護罩'},
                   {'name': '復活術', 'mp': 20, 'lv': 6, 'target': 'ally', 'eff': 'revive', 'val': 0.4,
                    'desc': '讓倒下的寵物以 40% HP 復活'}]},
    'mage':   {'name': '法師', 'hp': 95, 'mp': 50, 'ghp': 11, 'gmp': 7, 'spd': 20,
               'enc': 1.3, 'cap': 1.0, 'flee': 0.7, 'desc': '強化寵物魔法,改變戰場天氣',
               'skills': [
                   {'name': '魔力增幅', 'mp': 8, 'lv': 1, 'target': 'ally', 'eff': 'buff', 'st': 'matkup', 'dur': 15,
                    'desc': '我方寵物魔法攻擊力提升 35%,持續 15 秒'},
                   {'name': '烈日', 'mp': 12, 'lv': 3, 'target': 'none', 'eff': 'weather', 'val': 'sun', 'dur': 25,
                    'desc': '天氣變成烈日 25 秒:火、光屬性 +30%,水屬性 -20%'},
                   {'name': '暴雨', 'mp': 12, 'lv': 6, 'target': 'none', 'eff': 'weather', 'val': 'rain', 'dur': 25,
                    'desc': '天氣變成暴雨 25 秒:水、風屬性 +30%,火屬性 -30%'}]},
    'bard':   {'name': '吟遊詩人', 'hp': 100, 'mp': 45, 'ghp': 12, 'gmp': 6, 'spd': 25,
               'enc': 1.0, 'cap': 1.0, 'flee': 0.75, 'desc': '時間棒最快,用歌聲支援全隊',
               'skills': [
                   {'name': '魔力之歌', 'mp': 6, 'lv': 1, 'target': 'none', 'eff': 'mpall', 'val': 15,
                    'desc': '我方全體寵物恢復 MP'},
                   {'name': '安眠曲', 'mp': 10, 'lv': 3, 'target': 'enemy', 'eff': 'sleep', 'val': 0.65, 'dur': 6,
                    'desc': '65% 機率讓敵人睡著 6 秒 (被打會醒)'},
                   {'name': '戰歌', 'mp': 15, 'lv': 6, 'target': 'none', 'eff': 'hasteall', 'st': 'haste', 'dur': 15,
                    'desc': '我方全體寵物時間棒加快 35%,持續 15 秒'}]},
}

STATUS_NAMES = {'atkup': '攻↑', 'defup': '防↑', 'matkup': '魔↑', 'atkdown': '攻↓', 'defdown': '防↓',
                'slow': '緩', 'haste': '速', 'sleep': '睡', 'poison': '毒', 'guard': '防禦', 'shield': '盾',
                'protect': '護主'}

# ============================================================
#  道具
# ============================================================
ITEMS = {
    'red_potion':  {'name': '紅色藥水', 'type': 'use', 'hp': 80, 'price': 15, 'icon': 'potion', 'col': '#e03030',
                    'desc': '恢復寵物 HP 80'},
    'blue_potion': {'name': '藍色藥水', 'type': 'use', 'mp': 40, 'price': 25, 'icon': 'potion', 'col': '#3060e0',
                    'desc': '恢復寵物 MP 40'},
    'revive_herb': {'name': '復活草', 'type': 'use', 'revive': 0.3, 'price': 60, 'icon': 'herb', 'col': '#40c040',
                    'desc': '讓倒下的寵物以 30% HP 復活'},
    'seal_card':   {'name': '封印卡', 'type': 'seal', 'price': 30, 'icon': 'card', 'col': '#b890ff',
                    'desc': '戰鬥中對敵人使用,把牠封印成自己的寵物。對手血越少越容易成功'},
}
for _k, _sp in SPECIES.items():
    if 'egg' in _sp:
        ITEMS['egg_' + _k] = {'name': _sp['name'] + '蛋', 'type': 'egg', 'sp': _k, 'price': _sp['egg']['price'],
                              'icon': 'egg', 'col': ELEMENT_COLORS[_sp['el']],
                              'desc': '%s屬性的蛋。拿到孵化屋孵化吧!' % ELEMENTS[_sp['el']]}

# 寵物的食物 (每種寵物愛吃的不同,見 SPECIES 的 love / hate)
FOODS = {
    'meat':  {'name': '鮮肉', 'price': 8, 'col': '#d84a4a', 'desc': '新鮮的生肉。肉食的寵物最愛。'},
    'fish':  {'name': '鮮魚', 'price': 8, 'col': '#5a9ae0', 'desc': '剛釣上來的魚。'},
    'berry': {'name': '莓果', 'price': 5, 'col': '#c040a0', 'desc': '酸酸甜甜的野莓。'},
    'wheat': {'name': '麥穗', 'price': 5, 'col': '#e0b040', 'desc': '金黃色的麥穗。'},
    'wood':  {'name': '木材', 'price': 5, 'col': '#9a6a3a', 'desc': '乾燥的木頭……真的有寵物會吃嗎?'},
    'ore':   {'name': '礦石', 'price': 10, 'col': '#8a8aa0', 'desc': '亮晶晶的礦石。火屬性的寵物好像很喜歡。'},
}
for _k, _f in FOODS.items():
    ITEMS[_k] = {'name': _f['name'], 'type': 'food', 'price': _f['price'], 'icon': 'food_' + _k, 'col': _f['col'],
                 'desc': _f['desc'] + '雙擊餵給出戰寵物。'}

SHOP_ITEMS = ['red_potion', 'blue_potion', 'revive_herb', 'seal_card'] + list(FOODS)
EGG_SHOP = ['egg_' + k for k, sp in SPECIES.items() if 'egg' in sp and sp['egg'].get('shop', True)]

# ============================================================
#  寵物照顧 (飽食度、快樂值、親密度,範圍都是 0~100)
#  時間類的數值都是「每小時」,只算線上時間 (離線暫停)
# ============================================================
CARE = {
    # 起始值 (飽食度, 快樂值, 親密度)
    'start_new': (80, 70, 20), 'start_hatch': (70, 80, 30), 'start_wild': (50, 40, (0, 10)), 'start_old': (80, 70, 15),
    'start_breed': (70, 80, 40),   # 配對蛋孵出來的 (自己配出來的,比較親)
    'hungry': 30,              # 低於這個值 = 肚子餓
    'full': 90,                # 這個值以上吃不下
    'angry': 30,               # 快樂值低於這個值 = 鬧脾氣 (冒 💢 泡泡)
    'love_joy': 80, 'love_bond': 60,   # 春心蕩漾 ♥ 泡泡:快樂值、親密度都到這個值 (階段 3 接到發情)
    'hungry_mult': 0.9,        # 肚子餓時,戰鬥的攻擊/魔攻/防禦/魔防倍率
    'food_active': 15.0,       # 出戰寵物每小時消耗
    'food_other': 7.5,         # 身上其他寵物每小時消耗
    'food_battle': 0.5,        # 每場戰鬥 (有上場過的寵物)
    'joy_decay': 6.0,          # 快樂值每小時自然下降
    'joy_hungry': 60.0,        # 肚子餓時每小時額外下降
    'joy_starve': 120.0,       # 餓昏時每小時額外下降
    'joy_bank': 60.0,          # 寄放在旅館時每小時回升
    'starve_bond': -2,         # 餓昏 (飽食度歸零) 那一刻的親密度
    # 戰鬥 (快樂值, 親密度)
    'win': (1, 0.05), 'lose': (-10, 0), 'ko': (-5, -1), 'levelup': (10, 0),
    # 不聽指令:(快樂值低於, 機率);親密度會打折:× (1 - 親密度 / 200)
    'disobey': [(10, 0.30), (30, 0.15)],
    # 助攻 A:主人技能對自己的寵物 ×(1 + assist × 親密度/100)
    'assist': 0.5,
    # 助攻 B:默契量表
    'sync_bond': 40, 'sync_act': 6, 'sync_hit': 4, 'sync_power': 1.5,
    # 護主:連動傷害比例 (親密度 0 → 100),護主姿態
    'link_max': 0.15, 'link_min': 0.05,
    'guard_bond': 60, 'guard_enter': 0.30, 'guard_leave': 0.50, 'guard_def': 1.3,
    # 離家出走:快樂值與飽食度都是 0 持續幾秒 (只算線上、戰鬥外)
    'sulk_warn': 300, 'sulk_leave': 600, 'sulk_bond': -10, 'sulk_food': 40,
    'miss_you': 86400,         # 離線超過幾秒,上線時寵物會說想你
    'sleepy_idle': 20,         # 主人幾秒沒動,寵物開始打瞌睡
    'food_drop': 0.25,         # 野生寵物掉落最愛食物的機率
    'bank_max': 20,            # 寵物旅館可以寄放幾隻
}

# 餵食效果:口味 → (飽食度, 快樂值, 親密度)
TASTE = {'love': (35, 10, 4), 'like': (30, 5, 2), 'ok': (30, 2, 0), 'hate': (15, -8, 0)}
TASTE_NAMES = {'love': '最愛', 'like': '喜歡', 'ok': '普通', 'hate': '討厭'}

# 配對 (孵化屋的葛莉絲婆婆):發情 = 快樂值 ≥ CARE['love_joy']、親密度 ≥ CARE['love_bond']、沒有肚子餓
# 費用 = cost_base + cost_lv × 兩隻的平均等級;配完雙親快樂值 −joy_cost;婆婆最多保管 eggs_max 顆配對蛋
BREED = {'min_lv': 10, 'cost_base': 100, 'cost_lv': 10, 'joy_cost': 40, 'eggs_max': 3}
BREED_HINTS = [
    '聽說滿月的晚上,狼和狐狸會生下銀色的孩子……',
    '白天的鳥兒和夜晚的蝙蝠……黃昏的時候會發生什麼事呢?',
]

# 互動動作:快樂值、親密度、飽食度、冷卻秒數、條件
INTERACT = {
    'pet':   {'name': '摸摸', 'joy': 5, 'bond': 0.5, 'food': 0, 'cd': 180},
    'play':  {'name': '玩耍', 'joy': 15, 'bond': 1, 'food': -5, 'cd': 600, 'need_food': 10},
    'trick': {'name': '表演', 'joy': 3, 'bond': 0, 'food': 0, 'cd': 30, 'need_bond': 50},
}


def taste(sp, food):
    s = SPECIES[sp]
    if s.get('love') == '*':
        return 'like'
    if food == s.get('love'):
        return 'love'
    if food == s.get('hate'):
        return 'hate'
    return 'ok'


def assist_mult(bond):
    return 1 + CARE['assist'] * max(0, min(100, bond)) / 100.0


def link_ratio(bond):
    k = max(0, min(100, bond)) / 100.0
    return CARE['link_max'] - (CARE['link_max'] - CARE['link_min']) * k


def disobey_chance(joy, bond):
    for lim, ch in CARE['disobey']:
        if joy < lim:
            return ch * (1 - max(0, min(100, bond)) / 200.0)
    return 0.0


def sync_gain(base, bond):
    return base * (0.5 + max(0, min(100, bond)) / 100.0)


# ============================================================
#  美術:圖片在遊戲中的顯示大小 (256×256 畫布在畫面上的邊長,px) 與浮空高度
#  圖片放在 public/assets/pets/<種族>.webp,規格見 docs/art/美術規格.md、docs/phase-4/spec.md 第 3 節
# ============================================================
#  2026-10-10 實測:原本 (噗噗 48) 跟人物比起來太大,全部縮小約 30%,噗噗約等於程式繪圖的大小
ART = {
    'poring': {'size': 34}, 'slime': {'size': 36}, 'imp': {'size': 40, 'hover': 6}, 'goblin': {'size': 46},
    'wolf': {'size': 60}, 'skeleton': {'size': 52}, 'dove': {'size': 44, 'hover': 12}, 'fox': {'size': 60},
    'bat': {'size': 44, 'hover': 14}, 'griffin': {'size': 78}, 'drake': {'size': 68}, 'dragon': {'size': 160},
    'silverwolf': {'size': 60}, 'duskbird': {'size': 46, 'hover': 12},
    'npc': {'size': 56},
    'owner': {'size': 52},   # 主人圖 owners/<職業>-<m|f>.webp,男女一樣大 (spec 第 7、12 節)
}
for _k, _sp in SPECIES.items():   # 進化型態:初階的大小 × 1.15 / × 1.3
    if _sp['stage']:
        ART[_k] = dict(ART[_sp['line']], size=int(round(ART[_sp['line']]['size'] * _sp['look']['scale'])))
ART_FRAMES = ('attack', 'hurt', 'sleep')   # 可有可無的動作圖:<種族>_attack.webp …
OWNER_FRAMES = ('cast',)                   # 主人可有可無的動作圖:<職業>-<m|f>_cast.webp
ART_FRAME_NAMES = {'attack': '攻擊', 'hurt': '受傷', 'sleep': '睡著', 'cast': '施法'}   # 原圖檔名用中文:噗噗_攻擊.png
# 其他圖片的代號 → art-src/ 裡原圖的中文檔名
ART_UI = {'login': '登入畫面', 'logo': 'Logo'}
ART_GROUND = {'grass': '地面_草地', 'dark': '地面_森林草地', 'sand': '地面_沙路', 'stone': '地面_村莊石板',
              'ash': '地面_荒原焦土', 'water': '地面_水面'}
ART_DECO = {'tree_plain1': '草原樹1', 'tree_plain2': '草原樹2', 'tree_forest1': '森林樹1', 'tree_forest2': '森林樹2',
            'tree_dead': '荒原枯樹', 'rock1': '岩石1', 'rock2': '岩石2', 'bush': '草叢', 'flowers': '花叢'}

# ============================================================
#  孵蛋
# ============================================================
HATCH_TIME = 60          # 秒
HATCH_WARMUP = 20        # 前 20 秒是「預熱」,用來摸索,不計分
HATCH_HINTS = {
    'fire': '火屬性的蛋啊,最喜歡又熱又乾燥的地方。',
    'water': '水屬性的蛋喜歡溫和又潮濕……像雨後的森林那樣。',
    'light': '光屬性的蛋喜歡暖洋洋的,不過別太潮濕。',
    'dark': '暗屬性的蛋?牠們喜歡溫暖又悶濕的感覺。',
}

# ============================================================
#  遇敵區域 (依距離村莊中心的遠近)
#  mobs: (種族, 最低等級, 最高等級, 權重)    rare: (種族, 機率, 最低等級, 最高等級)
# ============================================================
ZONES = [
    {'name': '艾爾文草原', 'd': (0, 22), 'max': 2,
     'mobs': [('poring', 1, 2, 5), ('slime', 1, 3, 3)], 'rare': ('fox', 0.03, 3, 4)},
    {'name': '迷霧森林', 'd': (22, 32), 'max': 3,
     'mobs': [('slime', 4, 7, 2), ('goblin', 5, 8, 4), ('wolf', 6, 8, 2)], 'rare': ('dove', 0.03, 7, 8)},
    {'name': '狼嚎之丘', 'd': (32, 40), 'max': 3,
     'mobs': [('wolf', 8, 12, 4), ('goblin', 8, 10, 2), ('skeleton', 10, 13, 3)], 'rare': ('bat', 0.03, 11, 12)},
    {'name': '亡者荒原', 'd': (40, 99), 'max': 4,
     'mobs': [('skeleton', 13, 17, 4), ('wolf', 12, 15, 2), ('bat', 13, 16, 2)], 'rare': ('griffin', 0.02, 15, 16)},
]
ENCOUNTER_RATE = 0.045   # 每走一格的遇敵機率
ENCOUNTER_MIN_STEPS = 6  # 戰鬥結束後至少走幾格才會再遇敵
ROAD_ENCOUNTER = 0.35    # 走在道路上的遇敵倍率

# ============================================================
#  BOSS:炎龍
# ============================================================
BOSS = {'name': '炎龍', 'lv': 25, 'el': 'fire', 'hp': 3000, 'hp_per_player': 1200, 'mp': 999,
        'atk': 75, 'matk': 65, 'def': 20, 'mdef': 16, 'spd': 26, 'eva': 0.02,
        'exp': 1500, 'gold': 300, 'respawn': 180}
