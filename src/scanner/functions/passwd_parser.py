from typing import Iterator

import attr


@attr.s
class PasswdRecord:
    Name: str = attr.ib()
    Password: str = attr.ib()
    UID: int = attr.ib(converter=int)
    GID: int = attr.ib(converter=int)
    Gecos: str = attr.ib()
    HomeDirectory: str = attr.ib()
    Shell: str = attr.ib()


class PasswdParser:
    def __init__(self, content: str):
        self.content = content

    def __iter__(self) -> Iterator:
        self._iter = iter(self.content.splitlines())
        return self

    def __next__(self) -> PasswdRecord:
        line = next(self._iter)
        while not line.strip():
            line = next(self._iter)
        return PasswdRecord(*line.split(':'))
