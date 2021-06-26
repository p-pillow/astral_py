# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Iterable, Union

from Objects.Effects import ALL_EFFECTS
from Objects.Spells import get_all_spells

class Player:
    """The Player class which stores all information for every player.
    """
    def __init__(self, name: str,
                 start_spells: Union[dict, Iterable],
                 max_health_points: int=30,
                 health_points: int=0,
                 mana_points: int=0,
                 armor: int=0) -> None:
        """For creating a player there should be his name. Another properties have default values.
        Start health and mana points of a player are max_health_points, max mana points are max_health_points + 10.

        Args:
            name (str): A name of a player. Must be a string.
            max_health_points (int, optional): The maximum value of players health. Defaults to 30.
            armor (int, optional): Start armor points. Defaults to 0.

        Raises:
            ValueError: If a name is not a string.
        """
        if not isinstance(name, str):
            raise ValueError(f"Player's name must be a string, not {type(name)}")
        self._name = name
        self._max_health_points = max_health_points
        self._health_points = health_points if health_points > 0 else max_health_points
        self._mana_points = mana_points if mana_points > 0 else max_health_points
        self._armor = armor
        # spells of each player saves in the dict, where a key is a index of a spell and a value is its count
        if isinstance(start_spells, dict):
            self._spells = start_spells
        elif isinstance(start_spells, Iterable):
            self._spells = dict()
            for spell in start_spells:
                if spell in self._spells:
                    self._spells[spell] += 1
                else:
                    self._spells[spell] = 1
        else:
            raise ValueError(f"Wrong data used for player's spells initiate")
        # contain effects in a list as dicts with titles of effects as keys, values are dicts with:
        # timer: when an effect will be executed. If it < 0, it await, else it runs until timer < a duration of an effect
        # duration: how much an effect will work
        # is_locked: shows is an effect is cleanable. Not the same as is_clearable in an effect description 
        self._effects = list()

    def __repr__(self) -> str:
        return f"<Player {self._name}>"

    def __str__(self) -> str:
        return f"{self._name}: {self._health_points} hp, {self._mana_points} mp"

    def _check_points(self, points: int, message: str=""):
        if not isinstance(points, int) or points < 0:
            raise ValueError(message)

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_alive(self) -> bool:
        return self._health_points > 0

    @property
    def score(self) -> int:
        return self._health_points + self._mana_points if self.is_alive else 0

    @property
    def health_points(self) -> int:
        return self._health_points
    
    @property
    def mana_points(self) -> int:
        return self._mana_points 

    @property
    def max_mana_points(self) -> int:
        return self._max_health_points + 10

    def damage(self, points: int) -> None:
        """A method allows to damage a player. It not allows to set health points < 0.

        Args:
            points (int): A value of damage.
        """
        self._check_points(points, f"The value to damage should be >= 0, not {points}!")
        if self._health_points - points < 0:
            self._health_points = 0
        else:
            self._health_points -= points
    
    def heal(self, points: int) -> None:
        self._check_points(points, f"The value to heal should be >= 0, not {points}!")
        if self._health_points + points >= self._max_health_points:
            self._health_points = self._max_health_points
        else:
            self._health_points += points

    def add_max_hp(self, points: int) -> None:
        self._check_points(points, f"The value to add max hp should be >= 0, not {points}!")
        self._max_health_points += points

    def sub_max_hp(self, points: int) -> None:
        self._check_points(points, f"The value to sub max hp should be >= 0, not {points}!")
        self._max_health_points -= points

    def burn_mp(self, points: int) -> None:
        self._check_points(points, f"The value to burn mana points should be >= 0, not {points}!")
        self._mana_points -= points

    def restore_mp(self, points: int) -> None:
        self._check_points(points, f"The value to resore mana points should be >= 0, not {points}!")
        self._mana_points += points
        if self._mana_points > self.max_mana_points:
            self._mana_points = self.max_mana_points

    def add_armor(self, points: int) -> None:
        self._armor += points

    def kill(self) -> None:
        """This method allows to kill a player with removing all his effects.
        """
        self._health_points = 0
        self._mana_points = 0
        self._armor = 0
        self._effects.clear()

    def get_effects(self) -> list:
        return self._effects.copy()

    def add_effect(self, title: str, timer: int=0, duration: int=1, is_locked: bool=False) -> None:
        self._effects.append({"title": title, "timer": timer, "is_locked": is_locked, "duration": duration})

    def clean_effects(self, is_hard: bool=False) -> None:
        """Clean effects from a player. It can clean even not cleanable if is_hard is True.

        Args:
            is_hard (bool, optional): A flag to clean all effects. Defaults to False.
        """
        for e in self._effects.copy():
            if self._is_clearable(e["title"], is_hard):
                self._effects.remove(e)

    def remove_effect(self, title: str, is_hard=False) -> bool:
        for e in self._effects: # search an effect title
            if e["title"] == title and self._is_clearable(title, is_hard):
                self._effects.remove(e)
                return True
        return False

    def remove_oldest_effect(self, is_hard: bool=False) -> bool:
        for e in self._effects:
            if self._is_clearable(e["title"], is_hard):
                self._effects.remove(e)
                return True
        return False

    def remove_newest_effect(self, is_hard: bool=False) -> bool:
        for e in self._effects[::-1]:
            if self._is_clearable(e["title"], is_hard):
                self._effects.remove(e)
                return True
        return False

    def _is_clearable(self, title: str, is_hard: bool) -> bool:
        return is_hard or not self._effects[title]["is_locked"] and ALL_EFFECTS[title]["is_clearable"]

    def add_spell(self, spell_idx: int, count: int=1) -> None:
        if spell_idx not in get_all_spells():
            raise ValueError(f"There is no spell {spell_idx} for adding!")
        if count <=0:
            raise ValueError(f"Can't add less than 1 spell!")
        if spell_idx in self._spells:
            self._spells[spell_idx] += count
        else:
            self._spells[spell_idx] = count

    def remove_spell(self, spell_idx: int, count: int=1) -> None:
        if spell_idx not in get_all_spells():
            raise ValueError(f"There is no spell {spell_idx} for adding!")
        if count <=0:
            raise ValueError(f"Can't add less than 1 spell!")
        if spell_idx in self._spells:
            self._spells[spell_idx] -= count

    def clear_spells(self) -> None:
        self._spells.clear()

    def dump(self) -> dict:
        """Allows to save a player as a dict.

        Returns:
            dict: A dict with all players info.
        """
        return {
            "max_health_points" : self._max_health_points,
            "health_points" : self._health_points,
            "mana_points" : self._mana_points,
            "armor" : self._armor,
            "effects" : self._effects
        }

    def load(self, stored_player: dict):
        """Loads all settings of a player from a dict.

        Args:
            stored_player (dict): A dict with player's properties.
        """
        self._max_health_points = int(stored_player["max_health_points"])
        self._health_points = int(stored_player["health_points"])
        self._mana_points = int(stored_player["mana_points"])
        self._armor = int(stored_player["armor"])
        self._effects = OrderedDict(stored_player["effects"])
