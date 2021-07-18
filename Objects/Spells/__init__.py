# -*- coding: utf-8 -*-

from __future__ import annotations

from functools import cache
from math import log
from typing import TYPE_CHECKING

from Objects.Spells.functions import *

if TYPE_CHECKING:
    from Objects.Player import Player

class Spell_targets:
    SELF = 0
    DIRECTED = 1
    MASSIVE = 2
    ALL = 3
    ALLY = 4
    ENEMY = 5

class Spell_types:
    ALL = 0
    ATTACK = 1
    DEFENCE = 2


ALL_SPELLS = {
    0: {
        # meditation
        1 :{"priority": 21, "target_type": Spell_targets.SELF, "func": meditation},
        # run
        2: {"priority": 18, "target_type": Spell_targets.SELF, "func": run},
        # defence
        3: {"priority": 20, "target_type": Spell_targets.SELF, "func": defence},
        # levitation
        4: {"priority": 20, "target_type": Spell_targets.SELF, "func": fly},
        # suicide
        5: {"priority": 1,  "target_type": Spell_targets.SELF, "func": suicide},
        # fortune
        6: {"priority": 24, "target_type": Spell_targets.SELF, "func": shuffle_spells},
        # first aid
        7: {"priority": 23, "target_type": Spell_targets.SELF, "func": first_aid},
    },
    1: {
        1 : {"priority": 27, "type": Spell_types.ATTACK,  "works_in_stun": False,"target_type": (Spell_targets.DIRECTED, Spell_targets.ENEMY), "func": fire_arrow},
        2 : {"priority": 27, "type": Spell_types.ATTACK,  "works_in_stun": False,"target_type": (Spell_targets.DIRECTED, Spell_targets.ENEMY), "func": poison_spit},
        12: {"priority": 27, "type": Spell_types.DEFENCE, "works_in_stun": False,"target_type": (Spell_targets.DIRECTED, Spell_targets.ALLY), "func": healing},
        15: {"priority": 28, "type": Spell_types.ATTACK,  "works_in_stun": False,"target_type": (Spell_targets.DIRECTED, Spell_targets.ENEMY), "func": nightmare},
        19: {"priority": 22, "type": Spell_types.ALL,     "works_in_stun": False,"target_type": (Spell_targets.DIRECTED, ), "func": dispelling},
        24: {"priority": 21, "type": Spell_types.DEFENCE, "works_in_stun": False,"target_type": (Spell_targets.DIRECTED, Spell_targets.ALLY), "func": magic_shield},
    }
}

def use_spell(level: int, index: int, caster: Player=None, target: Player=None):
    if level in ALL_SPELLS:
        if index in ALL_SPELLS[level]:
            ALL_SPELLS[level][index]["func"](caster)
        else:
            raise ValueError(f"There is no index {index} of {level} level!")
    else:
        raise ValueError(f"There is no level {level}!")

@cache
def get_all_spells() -> list():
    all_spells_idx = list()
    for spell_lvl in ALL_SPELLS:
        for spell_idx in ALL_SPELLS[spell_lvl]:
            all_spells_idx.append((spell_lvl, spell_idx))
    return all_spells_idx

@cache
def get_spell_description(level: int, index: int):
    if level in ALL_SPELLS:
        if index in ALL_SPELLS[level]:
            return ALL_SPELLS[level][index].copy() # can't modify!
        else:
            raise ValueError(f"There is no {index} spell of {level} level!")
    else:
        raise ValueError(f"There is no {level} level of spells!")
