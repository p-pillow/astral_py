# -*- coding: utf-8 -*-

from typing import IO
from sys import stdin, stdout

class IO_handler:
    def __init__(self, in_stream: IO, out_stream: IO) -> None:
        self._i_stream = in_stream
        self._o_stream = out_stream

    def input(self, *args, **kwargs) -> str:
        raise NotImplementedError
    
    def print(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def get_move(self) -> dict:
        """Returns 3 components of a move: caster, spell and target.

        Returns:
            [type]: [description]
        """
        splitted_move = self.input().split(' ')
        if len(splitted_move) != 2 and len(splitted_move) != 3:
            return None
        return {
            splitted_move[0]: {
                "spell": splitted_move[1],
                "target": splitted_move[2] if len(splitted_move) >= 3 else None
            }
        }

class Std_IO_handler(IO_handler):
    def __init__(self) -> None:
        super().__init__(stdin, stdout)

    def input(self, *args, **kwargs) -> str:
        return self._i_stream.readline(*args, **kwargs).rstrip()

    def print(self, *args, **kwargs) -> None:
        self._o_stream.write(*args, **kwargs)
        self._o_stream.flush()
