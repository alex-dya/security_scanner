import attr

from scanner.functions.parsers import SplitLinesParserBase

@attr.s
class PasswdRecord:
    Name: str = attr.ib()
    Password: str = attr.ib()
    UID: int = attr.ib(converter=int)
    GID: int = attr.ib(converter=int)
    Gecos: str = attr.ib()
    HomeDirectory: str = attr.ib()
    Shell: str = attr.ib()


class PasswdParser(SplitLinesParserBase):
    TypeRecord = PasswdRecord

    def process_line(self, line):
        return line.split(':')
