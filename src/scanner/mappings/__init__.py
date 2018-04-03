from collections import UserDict
from scanner.const import os


class Mapping(UserDict):
    def __call__(self, key):
        return self.__getitem__(key)

    def __missing__(self, key):
        return None


unameOS = Mapping(
    {
        'Linux': os.LINUX,
        'SunOS': os.SOLARIS,
        'HP-UX': os.HPUX,
        'FreeBSD': os.FREEBSD,
        'AIX': os.AIX
    }
)

