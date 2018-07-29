from shlex import split
from typing import AnyStr, Iterable

import attr

from scanner.functions.parsers import SplitLinesParserBase


@attr.s
class InittabRecord:
    Id: str = attr.ib()
    Levels: str = attr.ib(converter=lambda x: x or '0123456')
    Action: str = attr.ib()
    Command: list = attr.ib(converter=split)


class InittabParser(SplitLinesParserBase):
    TypeRecord = InittabRecord

    def process_line(self, line: AnyStr) -> Iterable:
        if line.strip().startswith('#'):
            return []

        return line.split(':')
