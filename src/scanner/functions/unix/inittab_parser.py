from shlex import split
from typing import AnyStr, Iterable

import attr

from scanner.functions.parsers import SplitLinesParserBase
from scanner.functions.common import delete_comments


@attr.s
class InittabRecord:
    Id: str = attr.ib()
    Levels: str = attr.ib(converter=lambda x: x or '0123456')
    Action: str = attr.ib()
    Command: list = attr.ib(converter=split)


class InittabParser(SplitLinesParserBase):
    TypeRecord = InittabRecord

    @staticmethod
    def preprocess_content(content):
        return delete_comments(content)

    def process_line(self, line: AnyStr) -> Iterable:
        return line.split(':')
