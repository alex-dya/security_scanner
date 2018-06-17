from datetime import date
from typing import Iterator, AnyStr
from functools import partial

import attr


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


class ShadowParser:
    def __init__(self, content: str):
        self.content = content

    def __iter__(self) -> Iterator:
        self._iter = iter(self.content.splitlines())
        return self

    def __next__(self) -> ShadowRecord:
        line = next(self._iter)
        while not line.strip():
            line = next(self._iter)

        return ShadowRecord(*line.split(':'))
