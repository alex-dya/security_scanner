from datetime import datetime

import attr

from scanner.functions.parsers import SplitLinesParserBase
from scanner.mappings import UnixFileTypeMapping


@attr.s(slots=True, frozen=True)
class StatsRecord:
    Type: str = attr.ib(converter=UnixFileTypeMapping)
    Permissions: int = attr.ib(converter=lambda x: int(x, base=8))
    Owner: str = attr.ib()
    GroupOwner: str = attr.ib()
    Size: int = attr.ib(converter=int)
    ModifyDateTime: datetime = attr.ib(
        converter=lambda x: datetime.fromtimestamp(int(x)))
    Name: str = attr.ib()


class StatsParser(SplitLinesParserBase):
    TypeRecord = StatsRecord

    def process_line(self, line):
        return line.split('|')
