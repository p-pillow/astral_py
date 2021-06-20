from typing import Set, Iterable

from .Player import Player


class Team:
    #TODO: write Team class docstring
    def __init__(self, title: str, *members: Player) -> None:
        #TODO: write Team init docstring
        if not isinstance(title, str):
            raise ValueError(f"Team's title must be a string, not {type(title)}")
        self._title: str = title
        self._members: Set[Player] = {*members}

    def __len__(self):
        #TODO: write Team len docstring
        return len(self._members)
    
    def __getitem__(self, title: str) -> Player:
        #TODO: write Team getitem docstring
        for p in self._members:
            if p.name == title:
                return p
        raise ValueError(f"In {self._title} team no player with title {title}")

    def __repr__(self) -> str:
        #TODO: write Team repr docstring
        return f"<Team {self._title}>"

    def __str__(self) -> str:
        #TODO: write Team str docstring
        members_str = ',\n\t'.join(str(p) for p in self._members)
        return f"Team {self._title}:\n\t{members_str}"

    @property
    def title(self) -> str:
        #TODO: write Team title docstring
        return self._title

    def add(self, member: Player) -> None:
        #TODO: write Team add docstring
        if isinstance(member, Player):
            self._members.add(member)
        else:
            raise ValueError(f"You try to add not a Player: {member}")

    @property
    def alive_members(self) -> Set[Player]:
        #TODO: write Team alive docstring
        return {p for p in self._members if p.is_alive}

    @property
    def members(self) -> Set[Player]:
        #TODO: write Team alive docstring
        return self._members.copy()

    def get_score(self) -> int:
        return sum(p.score for p in self._members if p.is_alive)
