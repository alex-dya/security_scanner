import re
from .parsers import FinditerBase


class MountFinditer(FinditerBase):
    pattern = r'''
        ^
        (?P<Device>\S+)\s+
        on \s+
        (?P<Path>\S+)\s+
        type \s+
        (?P<Type>\S+)\s+
        \( (?P<Options>.*) \)\s*
        $
    '''

    flags = re.MULTILINE | re.VERBOSE
