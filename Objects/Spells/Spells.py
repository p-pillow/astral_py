from . import Player

SPELLS_TYPES = {
    "SELF": 0,
    "DIRECTED_ENEMY": 1,
    "DIRECTED_ALLY": 2,
    "MASSIVE_ENEMY": 3,
    "MASSIVE_ALLY": 4,
    "ALL" : 5
}

def common_spell(player: Player, **kwargs):
    if kwargs.get("add_mp"):
        player.restore_mp(kwargs.get("add_mp"))
    if kwargs.get("burn_mp"):
        player.burn_mp(kwargs.get("burn_mp"))
    if kwargs.get("heal_hp"):
        player.heal(kwargs.get("heal_hp"))
    if kwargs.get("damage"):
        player.damage(kwargs.get("damage"))
    if kwargs.get("add_armory"):
        player.damage(kwargs.get("add_armory"))
    if kwargs.get("effects"):
        for eff in kwargs.get("effects"):
            player.add_effect(eff)

ALL_SPELLS = [
    {"idx": 1, "level": 0, "title": "Meditation", "priority": 21, "type": SPELLS_TYPES["SELF"], "func": common_spell, "kwargs": {"add_mp": 3, "effects": ("Mana resist", "Prophecy")}},
    {"idx": 2, "level": 0, "title": "Run",        "priority": 18, "type": SPELLS_TYPES["SELF"], "func": common_spell, "kwargs": {"add_armory": 1, "effects": ("Run", )}},
]

def get_spell(spell_idx: int, spell_lvl: int):
    for spell in ALL_SPELLS:
        if spell["level"] == spell_lvl and spell["level"] == spell_idx:
            return spell
    raise ValueError(f"There is no spell with idx {spell_idx} of level {spell_lvl}")
