# -*- coding: utf-8 -*-

from typing import IO
from sys import stdin, stdout

class IO_handler:
    def input(self, *args, **kwargs) -> str:
        raise NotImplementedError
    
    def print(self, *args, **kwargs) -> None:
        raise NotImplementedError

class Std_IO_handler(IO_handler):
    def __init__(self, in_stream: IO=stdin, out_stream: IO=stdout) -> None:
        self._i_stream = in_stream
        self._o_stream = out_stream

    def input(self, *args, **kwargs) -> str:
        return self._o_stream.readline(*args, **kwargs).rstrip()

    def print(self, *args, **kwargs) -> None:
        self._o_stream.write(*args, **kwargs)
        self._o_stream.flush()
