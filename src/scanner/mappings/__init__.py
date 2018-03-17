from collections import UserDict
from scanner.const import OS


class Mapping(UserDict):
    def __call__(self, key):
        return self.__getitem__(key)

    def __missing__(self, key):
        return None


unameOS = Mapping(
    {
        'Linux': OS.LINUX,
        'SunOS': OS.SOLARIS,
        'HP-UX': OS.HPUX,
        'FreeBSD': OS.FREEBSD,
        'AIX': OS.AIX
    }
)

