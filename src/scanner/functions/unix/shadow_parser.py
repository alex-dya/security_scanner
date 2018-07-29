from datetime import date
from typing import Iterator, AnyStr
from functools import partial

import attr

from scanner.functions.parsers import SplitLinesParserBase

MAX = 99999


def int_or(x: AnyStr, default: int) -> int:
    if x:
        return int(x)
    return default


int_or_max=partial(int_or, default=MAX)
int_or_zero=partial(int_or, default=0)


@attr.s
class ShadowRecord:
    Name: str = attr.ib()
    Password: str = attr.ib()
    PasswordChange: date = attr.ib(
        converter=lambda x: date.fromtimestamp(int(x) * 86400)
    )
    MinPasswordAge: int = attr.ib(converter=int_or_zero)
    MaxPasswordAge: int = attr.ib(converter=int_or_max)
    PasswordWarn: int = attr.ib(converter=int_or_zero)
    PasswordExpired: int = attr.ib(converter=int_or_max)
    AccountExpired: int = attr.ib(converter=int_or_max)
    ReservedField: str = attr.ib()


class ShadowParser(SplitLinesParserBase):
    TypeRecord = ShadowRecord

    def process_line(self, line):
        return line.split(':')
