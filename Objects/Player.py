from logging import setLoggerClass


class Player:
    #TODO: write Player class docstring
    def __init__(self, name: str, max_health_points: int=30, armor: int=0) -> None:
        #TODO: write Player init docstring
        if not isinstance(name, str):
            raise ValueError(f"Player's name must be a string, not {type(name)}")
        self._name = name
        self._max_health_points = max_health_points
        self._health_points = max_health_points
        self._mana_points = max_health_points
        self._armor = armor
        self._effects = list()

    def __repr__(self) -> str:
        #TODO: write Player repr docstring
        return f"<Player {self._name}>"

    def __str__(self) -> str:
        #TODO: write Player str docstring
        return f"{self._name}: {self._health_points} hp, {self._mana_points} mp"

    @property
    def name(self) -> str:
        #TODO: write Player name docstring
        return self._name

    @property
    def is_alive(self) -> bool:
        return self._health_points > 0

    @property
    def score(self) -> int:
        return self._health_points + self._mana_points

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
        if self._health_points - points < 0:
            self._health_points = 0
        else:
            self._health_points -= points
    
    def heal(self, points: int) -> None:
        if self._health_points + points >= self._max_health_points:
            self._health_points = self._max_health_points
        else:
            self._health_points += points

    def burn_mp(self, points: int) -> None:
        self._mana_points -= points

    def restore_mp(self, points: int) -> None:
        self._mana_points 

    def kill(self) -> None:
        self._health_points = 0

    def add_effect(self, effect) -> None:
        self._effects.append(effect)
