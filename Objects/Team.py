# -*- coding: utf-8 -*-

from typing import Dict

from Objects.Player import Player


class Team:
    #TODO: write Team class docstring
    def __init__(self, title: str, *members: Player) -> None:
        #TODO: write Team init docstring
        if not isinstance(title, str):
            raise ValueError(f"Team's title must be a string, not {type(title)}")
        self._title: str = title
        self._members: Dict[Player] = dict()
        for m in members:
            self._members[m.name] = m
            m.set_team(self)

    def __len__(self):
        return len(self._members)
    
    def __getitem__(self, name: str) -> Player:
        """Allows to get a member of a team by his name.

        Args:
            name (str): A name of a member.

        Raises:
            ValueError: If there is no member with a given name.

        Returns:
            Player: A member of a team.
        """
        if name in self._members:
            return self._members[name]
        else:
            raise ValueError(f"In {self._title} team no player with name {name}")

    def __iter__(self):
        return iter(self._members.keys())

    def __repr__(self) -> str:
        return f"<Team {self._title}>"

    def __str__(self) -> str:
        members_str = ',\n\t'.join(str(self._members[p]) for p in self._members)
        return f"Team {self._title}:\n\t{members_str}"

    @property
    def title(self) -> str:
        return self._title

    def add(self, member: Player) -> None:
        if not isinstance(member, Player):
            raise ValueError(f"You try to add not a Player: {member}")
        elif member.name in self._members:
            raise ValueError(f"A Player {member.name} is already in the team")
        else:
            self._members[member.name] = member
            member.set_team(self)

    def get_score(self) -> int:
        return sum(self._members[name].score for name in self._members)
    
    def get_alive_members(self) -> list:
        return [name for name in self._members.copy() if self._members[name].is_alive]  

    def get_active_members(self) -> list:
        """Returns a list with active members names.

        Returns:
            list: A list with active members names.
        """
        return [name for name in self._members.copy() if self._members[name].can_move()]
    
    def get_members(self) -> list:
        """Returns a list with members names.

        Returns:
            list: A list with members names.
        """
        return list(self._members.keys())
