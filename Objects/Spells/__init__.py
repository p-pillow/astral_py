# -*- coding: utf-8 -*-

from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING

from Objects.Spells.functions import *

if TYPE_CHECKING:
    from Objects.Player import Player

SPELLS_TYPES = {
    "SELF": 0,
    "DIRECTED_ENEMY": 1,
    "DIRECTED_ALLY": 2,
    "MASSIVE_ENEMY": 3,
    "MASSIVE_ALLY": 4,
    "ALL" : 5
}

ALL_SPELLS = {
    0: {
        # meditation
        1 :{"priority": 21, "type": SPELLS_TYPES["SELF"], "func": meditation},
        # run
        2: {"priority": 18, "type": SPELLS_TYPES["SELF"], "func": run},
        # defence
        3: {"priority": 20, "type": SPELLS_TYPES["SELF"], "func": defence},
        # levitation
        4: {"priority": 20, "type": SPELLS_TYPES["SELF"], "func": fly},
        # suicide
        5: {"priority": 1,  "type": SPELLS_TYPES["SELF"], "func": suicide},
        # fortune
        6: {"priority": 24, "type": SPELLS_TYPES["SELF"], "func": shuffle_spells},
        # first aid
        7: {"priority": 23, "type": SPELLS_TYPES["SELF"], "func": first_aid},
    },
    1: {
        1: {"priority": 18, "type": SPELLS_TYPES["SELF"], "func": fire_arrow},
    }
}

def use_spell(spell_idx: int, spell_lvl: int, caster: Player):
    if spell_lvl in ALL_SPELLS:
        if spell_idx in ALL_SPELLS[spell_lvl]:
            ALL_SPELLS[spell_lvl][spell_idx]["func"](caster)
        else:
            raise ValueError(f"There is no index {spell_idx} of {spell_lvl} level!")
    else:
        raise ValueError(f"There is no level {spell_lvl}!")

@cache
def get_all_spells() -> list():
    all_spells_idx = list()
    for spell_lvl in ALL_SPELLS:
        for spell_idx in ALL_SPELLS[spell_lvl]:
            if spell_lvl == 0:
                continue
            if spell_idx < 10:
                all_spells_idx.append(spell_lvl*10 + spell_idx)
            else:
                all_spells_idx.append(spell_lvl*100 + spell_idx)
    return all_spells_idx
