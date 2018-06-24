import re
from .parsers import FinditerBase, FinditerMatchObject


class MountMatchObject(FinditerMatchObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dict['Options'] = [
                opt.strip()
                for opt in self.Options.split(',')
            ]


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

    def __next__(self) -> MountMatchObject:
        return MountMatchObject(match_object=next(self._iter))
