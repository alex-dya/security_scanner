from typing import NamedTuple
from datetime import date, timedelta


class ShadowRecord(NamedTuple):
    Name: str
    Password: str
    PasswordChange: date
    MinPasswordAge: int
    MaxPasswordAge: int
    PasswordWarn: int
    PasswordExpired: int
    AccountExpired: int
    ReservedField: str

    def __init__(self, name, password, change, *args, **kwargs):
        change = date(1970, 1, 1) + timedelta(days=int(change))
        super().__init__(name, password, change, *args, **kwargs)


class ShadowParser:
    def __init__(self, content: str):
        self.content = content

    def __iter__(self):
        self._iter = iter(self.content.splitlines())
        return self

    def __next__(self):
        record = ShadowRecord(*next(self._iter).split(':'))
        return record
