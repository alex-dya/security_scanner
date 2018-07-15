import re
from typing import Tuple

import attr

from .parsers import FinditerMatchObject, FinditerBase
from scanner.functions.common import split_and_strip


@attr.s(slots=True, frozen=True)
class LsmodRecord(FinditerMatchObject):
    Name: str = attr.ib()
    Size: int = attr.ib(converter=int)
    Number: int = attr.ib(converter=int)
    Modules: Tuple[str] = attr.ib(
        converter=lambda data: split_and_strip(data, delimiter=',') or tuple(),
    )


class LsmodParser(FinditerBase):
    pattern = r'''
        ^
        (?P<Name>\w+)\s+
        (?P<Size>\d+)\s+
        (?P<Number>\d+)
        (\s+ (?P<Modules>[\w,]+) )?
        $
    '''

    flags = re.MULTILINE | re.VERBOSE

    def __next__(self) -> LsmodRecord:
        return LsmodRecord(**next(self._iter).groupdict())
