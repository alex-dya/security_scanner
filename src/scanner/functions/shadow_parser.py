from datetime import date
from typing import Iterator, AnyStr


class ShadowRecord:
    Name: str
    Password: str
    PasswordChange: date
    MinPasswordAge: int
    MaxPasswordAge: int
    PasswordWarn: int
    PasswordExpired: int
    AccountExpired: int
    ReservedField: str

    def __init__(self, name, passwd, change, minpass, maxpass,
                 passwarn, passexp, accexp, reserved):
        super().__init__()
        self.Name = name
        self.Password = passwd
        self.PasswordChange = date.fromtimestamp(int(change) * 86400)
        self.MinPasswordAge = minpass and int(minpass) or 0
        self.MaxPasswordAge = maxpass and int(maxpass) or 99999
        self.PasswordWarn = passwarn and int(passwarn) or 0
        self.PasswordExpired = passexp and int(passexp) or 99999
        self.AccountExpired = accexp and int(accexp) or 99999
        self.ReservedField = reserved

    def __repr__(self) -> AnyStr:
        return f'ShadowRecord({self.Name}, {self.Password})'


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
