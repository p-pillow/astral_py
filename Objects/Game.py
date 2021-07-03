# -*- coding: utf-8 -*-

import logging
import random
from itertools import chain
from datetime import datetime
from typing import Dict, Iterable, Set, Union, cast

from Objects.Team import Team
from Objects.IO_handler import IO_handler, Std_IO_handler
from Objects.Player import Player
from Objects.Localization import RUS_TEXTS
from Objects.Spells import get_all_spells


class Game:
    def __init__(self,
                teams: Union[Dict[str, Iterable[str]], Iterable[Team]]=None,
                teams_num: int=2,
                team_size: int=1,
                rounds: int=30,
                loglevel: int=logging.WARNING,
                io_handler: IO_handler=Std_IO_handler(),
                random_seed: int=0,
                message_splitter: str="\n",
                messages: dict=RUS_TEXTS,
                **player_kwargs) -> None:
        """Main class, which manages teams, spells, moves of players and etc.

        Args:
            teams (Union[Dict[str, Dict], Iterable[Team]], optional): Teams can be created before Game class.
            It can be a set with ready teams or just dict, where keys are team title, and values are iterable objects with players names.
            Also it can be iterable object with Teams. If not set, teams will be created in the beginning interactively. Defaults to None.
            teams_num (int, optional): A number of teams. Used while creating teams. If 0, it will be asked. Defaults to 2.
            team_size (int, optional): A number of players in each team. Used while creating teams. If 0, it will be asked. Defaults to 1.
            rounds (int, optional): A number of rounds. Defaults to 30.
            loglevel (int, optional): A level of logging. Defaults to logging.WARNING.
            io_handler (IO_handler, optional): Hadler for comfortable IO. Can be overwritten. Defaults to Std_IO_handler().

        Raises:
            ValueError: If teams is Iterable and consists not Team objects.
        """
        self._logger = logging.Logger(name=f"Game {datetime.now()}", level=loglevel)
        self._logger.debug("Logger created")
        random.seed(random_seed)
        self._logger.debug(f"Random seed is {random_seed}")
        self._io_handler = io_handler
        self._rounds = rounds
        self._messages = messages
        self._message_splitter = message_splitter
        # initial spells
        player_kwargs["start_spells"] = {11, 112, 119, 124}
        if isinstance(teams, dict): # make teams from a dict with names
            self._teams: Set[Team] = self.make_teams_from_dict(teams)
        elif isinstance(teams, Iterable): # teams already created
            # additional check what there are Teams
            for t in teams:
                if not isinstance(t, Team):
                    raise ValueError(f"Iterable object have to consist Team, not {type(t)}")
            self._teams: Set[Team] = set(teams)
        else: # create teams
            self._teams: Set[Team] = self.make_teams(teams_num, team_size, io_handler, **player_kwargs)
        

    def run(self) -> None:
        """Runs the game.
        """
        for round_num in range(1, self._rounds+1):
            self.print(self._messages["events"]["new_round"].format(round_num))
            # get moves of players
            moves = self.get_moves()
            print(moves)
        # the end of a game
        winners = self.get_winners()
        if len(winners) == 1:
            self.print(self._messages["events"]["winner"].format(str(self.get_team(next(iter(winners))))))
        else:
            winners_str = '\n'.join((str(self.get_team(t)) for t in sorted(winners)))
            self.print(self._messages["events"]["draw"].format(winners_str))

    def get_winners(self) -> set[Team]:
        """Select winners. If 1 team has more alive players, it win, else count by points

        Returns:
            set[Team]: Set of winners.
        """
        winners = dict()
        max_score = 0
        for t in self._teams:
            if t.get_score() > max_score:
                winners.clear()
                max_score = t.get_score()
            if t.get_score() == max_score:
                winners[t.title] = max_score
        return winners

    def get_team(self, title):
        for t in self._teams:
            if title == t.title:
                return t
        raise ValueError(f"No such team: {title}")

    def get_all_players(self, only_alive: bool=False) -> list:
        return [p.name for p in chain.from_iterable(self._teams) if not only_alive or only_alive and p.is_alive]

    def get_moves(self) -> dict:
        moves = dict()
        # get names of players what can move
        players_can_move = list()
        for t in self._teams:
            players_can_move.extend(t.get_active_members())
        # get all moves
        self.print(self._messages["events"]["ask_move"])
        while len(moves) != len(players_can_move):
            move = self._io_handler.get_move()
            if not move:
                self._logger.warning(self._messages["warnings"]["empty_move"])
                continue
            caster = next(iter(move)) # a move contains just one key
            # check caster's name
            if caster not in self.get_all_players():
                self._logger.warning(self._messages["warnings"]["player_not_exists"].format(caster))
                continue
            if caster not in players_can_move:
                self._logger.warning(self._messages["warnings"]["wrong_caster"].format(caster))
                continue
            if not move[caster]["spell"].isdigit():
                spell_idx = self.find_by_alias()
                if not spell_idx:
                    continue
                move[caster]["spell"] = spell_idx
            if move[caster]["spell"] not in get_all_spells():
                self._logger.warning(self._messages["warnings"]["spell_not_exists"].format(move[caster]["spell"]))
                continue
            if caster in moves:
                self.print(self._messages["events"]["move_updated"].format(caster, move[caster]["spell"], move[caster]["target"]))
            else:
                self.print(self._messages["events"]["move_saved"].format(caster, move[caster]["spell"], move[caster]["target"]))
            moves.update(move)
        return moves

    def find_by_alias(self, alias: str) -> str:
        for level in self._messages["spells"]:
            for spell_idx in self._messages["spells"][level]:
                if self._messages["spells"][level][spell_idx]["alias"] == alias:
                    return f"{level}{spell_idx}"
        self._logger.warning(f"")
        return None

    def input(self, *args, **kwargs) -> None:
        self._io_handler.input(*args, **kwargs)
    
    def print(self, message) -> None:
        self._io_handler.print(f"{message}{self._message_splitter}")

    @staticmethod
    def make_teams_from_dict(teams_dict: Dict[str, Iterable[str]], **player_kwargs) -> Set[Team]:
        """Makes set of teams from dict.

        Args:
            teams_dict (Dict[str, Dict]): dict with its title and Iterable with players names.

        Returns:
            Set[Team]: Set with Team objects.
        """
        return {Team(t_title, *{Player(p_name, **player_kwargs) for p_name in teams_dict[t_title]}) for t_title in teams_dict}

    @staticmethod
    def make_teams(teams_num: int=0, team_size: int=0, io_handler: IO_handler=Std_IO_handler(), **p_kwargs) -> Set[Team]:
        # TODO: write docstring
        """[summary]

        Args:
            teams_num (int, optional): [description]. Defaults to 0.
            team_size (int, optional): [description]. Defaults to 0.
            io_handler (IO_handler, optional): [description]. Defaults to Std_IO_handler().

        Returns:
            Set[Team]: [description]
        """
        teams: Set[Team] = set()
        while not teams_num:
            io_handler.print("Input a number of teams: ")
            teams_num_str: str = io_handler.input()
            if teams_num_str.isalnum() and int(teams_num_str) > 1:
                teams_num = int(teams_num_str)
        while not team_size:
            io_handler.print("Input a number of members in every team: ")
            team_size_str: str = io_handler.input()
            if team_size_str.isalnum() and int(team_size_str) > 0:
                team_size = int(team_size_str)
        for _ in range(teams_num):
            io_handler.print("Input a name of a team: ")
            t_name = io_handler.input()
            team = Team(t_name)
            for _ in range(team_size):
                io_handler.print("Input a name of a player: ")
                team.add(Player(io_handler.input(), **p_kwargs))
        return teams
