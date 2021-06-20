# -*- coding: utf-8 -*-

from logging import setLoggerClass
from .Effects import ALL_EFFECTS

class Player:
    """The Player class which stores all information for every player.
    """
    def __init__(self, name: str, max_health_points: int=30, armor: int=0) -> None:
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
        self._health_points = max_health_points
        self._mana_points = max_health_points
        self._armor = armor
        # effects list contain a dicts with indexes of effects, its duration and possibility of clearing
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

    def burn_mp(self, points: int) -> None:
        self._check_points(points, f"The value to burn mana points should be >= 0, not {points}!")
        self._mana_points -= points

    def restore_mp(self, points: int) -> None:
        self._check_points(points, f"The value to resore mana points should be >= 0, not {points}!")
        self._mana_points 

    def kill(self) -> None:
        """This method allows to kill a player with removing all his effects.
        """
        self._health_points = 0
        self._mana_points = 0
        self._armor = 0
        self._effects.clear()

    def add_effect(self, idx: int, duration: int=1, is_cleanable: int=True) -> None:
        self._effects.append({"idx": idx,
                              "duration": duration,
                              "is_cleanable": is_cleanable
                            })

    def clean_effects(self, hard: bool=False) -> None:
        """Clean effects from a player. It can clean even not cleanable if hard is True.

        Args:
            hard (bool, optional): A flag to clean all effects. Defaults to False.
        """
        for e in self._effects.copy():
            if hard or not (e["is_cleanable"] or ALL_EFFECTS[e["idx"]]["is_cleanable"]):
                self._effects.remove(e)

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
        self._max_health_points = stored_player["max_health_points"]
        self._health_points = stored_player["health_points"]
        self._mana_points = stored_player["mana_points"]
        self._armor = stored_player["armor"]
        self._effects = stored_player["effects"]
