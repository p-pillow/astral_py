# -*- coding: utf-8 -*-

import logging
import random
from datetime import datetime
from itertools import chain
from typing import Dict, Iterable, Set, Union

from Objects.IO_handler import IO_handler, Std_IO_handler
from Objects.Localization import RUS_TEXTS
from Objects.Player import Player
from Objects.Spells import Spell_targets, get_all_spells, get_spell_description, use_spell
from Objects.Team import Team


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
            self.print_message(("events", "new_round"), round_num)
            # get moves of players
            moves = self.get_moves()
            for caster_name in sorted(moves, key=lambda caster_name: get_spell_description(get_level(int(moves[caster_name]["spell"])), get_index(int(moves[caster_name]["spell"]))["priority"])):
                spell_level = get_level(moves[caster_name]["spell"])
                spell_index = get_index(moves[caster_name]["spell"])
                caster = self.search_player(caster_name)
                spell = get_spell_description(spell_level, spell_index)
                # check if a spell's targets should be few players
                if spell["target_type"] == Spell_targets.ALL or spell["target_type"] == Spell_targets.MASSIVE:
                    if isinstance(moves[caster_name]["target"], Iterable):
                        targets = [self.search_player(t) for t in moves[caster_name]["target"]]
                    else:
                        targets = self.search_player(moves[caster_name]["target"])
                else:
                    target = self.search_player(moves[caster_name]["target"])
                use_spell(spell_level, spell_index, caster, target)
                self.print_message(("spells", spell_level, spell_index))
        # the end of a game
        winners = self.get_winners()
        if len(winners) == 1:
            self.print_message(("events", "winner"), str(self.get_team(next(iter(winners)))))
        else:
            winners_str = '\n'.join((str(self.get_team(t)) for t in sorted(winners)))
            self.print_message(("events", "draw"), winners_str)

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

    def search_player(self, player_name: str) -> Player:
        for t in self._teams:
            if player_name in t:
                return t[player_name]
        return None

    def get_all_players(self, only_alive: bool=False) -> list:
        return [p.name for p in chain.from_iterable(self._teams) if not only_alive or only_alive and p.is_alive]

    def get_moves(self) -> dict:
        moves = dict()
        # get names of players what can move
        players_can_move = list()
        for t in self._teams:
            players_can_move.extend(t.get_active_members())
        # get all moves
        self.print_message(("events", "ask_move"))
        while len(moves) != len(players_can_move):
            move = self._io_handler.get_move()
            self._logger.debug(f"Input move: {move}")
            if not move:
                self.warning(("warnings", "empty_move"))
                continue
            caster = next(iter(move)) # a move contains just one key
            # check caster's name
            if caster not in self.get_all_players():
                self.warning(("warnings", "player_not_exists"), caster)
                continue
            if caster not in players_can_move:
                self.warning(("warnings", "wrong_caster"), caster)
                continue
            # make a spell as a tuple (spell_lvl, spell_idx)
            if move[caster]["spell"].isdigit():
                spell_lvl, spell_idx = int(move[caster]["spell"][0]), int(move[caster]["spell"][1:])
                move[caster]["spell"] = (spell_lvl, spell_idx)
            else:
                spell = self._messages["aliases"].get(move[caster]["spell"])
                move[caster]["spell"] = spell
            # check if a spell exists
            if move[caster]["spell"] not in get_all_spells():
                self.warning(("warnings", "spell_not_exists"), move[caster]["spell"])
                continue
            # target handling
            if move[caster].get("target"):
                # check if a spell can be used as a target
                if not self.check_target(caster, move[caster]["spell"], move[caster]["target"]):
                    self.warning(("warnings", "bad_target"), move[caster]["spell"], move[caster]["spell"])
                    continue
            else:
                # autotarget if it is possible
                pass
            if caster in moves:
                self.print_message(("events", "move_updated"), caster, move[caster]["spell"], move[caster]["target"])
            else:
                self.print_message(("events", "move_saved"), caster, move[caster]["spell"], move[caster]["target"])
            moves.update(move)
        return moves

    def check_target(self, caster_name, spell, target_name):
        if not target_name or not spell or not caster_name:
            return False
        spell_descr = get_spell_description(spell)
        caster_player = self.search_player(caster_name)
        target_player = self.search_player(target_name)
        if spell_descr["target_type"] == Spell_targets.SELF and caster_player != target_player:
            return False
        if spell_descr["target_type"] == (Spell_targets.DIRECTED, Spell_targets.ENEMY) and caster_player.team != target_player.team:
            return False
        if spell_descr["target_type"] == (Spell_targets.DIRECTED, Spell_targets.ALLY) and caster_player.team == target_player.team:
            return False
        return True

    def input(self, *args, **kwargs) -> None:
        self._io_handler.input(*args, **kwargs)

    def find_message(self, message_keys: Iterable) -> str:
        message_dict = self._messages
        for k in message_keys:
            if k in message_dict:
                message_dict = message_dict[k]
            else:
                self._logger.error(f"There is no {k} in {message_dict.keys()}")
                break
        return message_dict

    def print(self, *args, **kwargs):
        self._io_handler.print(*args, **kwargs)
    
    def print_message(self, message_keys: Iterable, *format_args, **format_kwargs) -> None:
        message = self.find_message(message_keys)
        self._io_handler.print(f"{message.format(*format_args, **format_kwargs)}{self._message_splitter}")

    def warning(self, message_keys: Iterable, *format_args, **format_kwargs) -> None:
        message = self.find_message(message_keys)
        self._logger.warning(message.format(*format_args, **format_kwargs))

    def error(self, message_keys: Iterable, *format_args, **format_kwargs) -> None:
        message = self.find_message(message_keys)
        self._logger.error(message.format(*format_args, **format_kwargs))

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
