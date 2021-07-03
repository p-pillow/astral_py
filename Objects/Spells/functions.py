# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

from Objects.Effects import ALL_EFFECTS
from utils import is_worked

if TYPE_CHECKING:
    from Objects.Player import Player

def meditation(p: Player) -> None:
    p.restore_mp(3)
    p.add_effect(ALL_EFFECTS["mana_resist"])
    p.add_effect(ALL_EFFECTS["prophecy"])

def run(p: Player) -> None:
    p.add_armor(1)
    p.add_effect(ALL_EFFECTS["falling"])

def fly(p: Player) -> None:
    p.restore_mp(1)
    p.add_effect(ALL_EFFECTS["levitate"])
    
def defence(p: Player) -> None:
    p.add_effect(ALL_EFFECTS["damage_resist"])
    effects = p.get_effects()
    if len(effects) >= 2 or is_worked(0.4):
        p.remove_oldest_effect() # remove 1 oldest effect

def suicide(p: Player) -> None:
    p.kill()

def first_aid(p: Player) -> None:
    p.add_max_hp(2)
    p.heal(4)

def shuffle_spells(p: Player) -> None:
    #TODO
    pass

def fire_arrow(p: Player) -> None:
    p.damage(6)
    p.add_effect(ALL_EFFECTS["burn"], -1)

def poison_spit(p: Player) -> None:
    p.add_effect(ALL_EFFECTS["poison"], 0, 4)

def healing(p: Player) -> None:
    p.add_effect(ALL_EFFECTS["healing"])

def nightmare(p: Player) -> None:
    p.add_effect(ALL_EFFECTS["nightmare"], -1, 1)

def dispelling(p: Player) -> None:
    p.clean_effects()

def magic_shield(p: Player) -> None:
    p.add_effect(ALL_EFFECTS["magic_shield"])
