from collections import UserDict
from scanner.const import OS


class Mapping(UserDict):
    def __call__(self, item):
        return self.__getitem__(item)


unameOS = Mapping(
    {
        'GNU/Linux': OS.LINUX,
        'SunOS': OS.SOLARIS,
        'HP-UX': OS.HPUX,
        'FreeBSD': OS.FREEBSD,
        'AIX': OS.AIX
    }
)

