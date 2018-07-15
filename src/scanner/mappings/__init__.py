from collections import UserDict
from scanner.const import os, file_type


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


UnixFileTypeMapping = Mapping(
    {
        'regular file': file_type.FILE,
        'regular empty file': file_type.FILE,
        'character special file': file_type.CHARACTER_DEVICE,
        'directory': file_type.DIRECTORY,
        'symbolic link': file_type.SYMLINK,
        'block special file': file_type.BLOCK_DEVICE,
        'fifo': file_type.FIFO,
        'socket': file_type.SOCKET
    }
)
