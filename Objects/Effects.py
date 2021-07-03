# -*- coding: utf-8 -*-

"""Description of all effects
    title - a title of an effect
    is_clearable - can this effect be cleared by simple clear
    type - buff or debuff
    reaction_time - it can work before a round, with action or after a round
"""

ALL_EFFECTS = {
    "mana_resist":   {"is_clearable": True, "type": "buff", "reaction_time": 0},
    "prophecy":      {"is_clearable": True, "type": "buff", "reaction_time": 0},
    "falling":       {"is_clearable": True, "type": "debuff", "reaction_time": 0},
    "levitate":      {"is_clearable": True, "type": "debuff", "reaction_time": 0},
    "damage_resist": {"is_clearable": True, "type": "debuff", "reaction_time": 0},
}
