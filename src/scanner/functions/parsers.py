import abc
import re
from typing import AnyStr, Iterator
from utility import AddLoggerMeta


class FinditerBaseMeta(abc.ABCMeta, AddLoggerMeta):
    pass


class KeyValueParser:
    double_quotes = re.compile(r'^".+"$')

    def __init__(self, text: str, delimiter: str = '='):
        self.text = text
        self.delimiter = delimiter
        self.result = dict()
        self.__process()

    def __process(self) -> None:
        for line in self.text.splitlines():

            if not line.strip():
                continue

            key, _, value = map(str.strip, line.partition(self.delimiter))

            if self.double_quotes.match(value):
                value = value[1:-1]

            if key in self.result:
                if isinstance(self.result[key], list):
                    self.result[key] = self.result[key] + [value]
                else:
                    self.result[key] = [self.result[key]] + [value]
            else:
                self.result[key] = value

    def __getattr__(self, item: str) -> AnyStr:
        if item in self.result:
            return self.result[item]
        else:
            raise AttributeError


class FinditerMatchObject(metaclass=AddLoggerMeta):
    def __init__(self, match_object: re.match):
        self.match = match_object
        self.dict = match_object.groupdict()

    def __getattr__(self, item: str) -> AnyStr:
        if item in self.dict:
            return self.dict[item]
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        if key not in ('match', 'dict'):
            raise RuntimeError('It is immutable object')

        self.__dict__[key] = value

    def __str__(self) -> AnyStr:
        return f'{self.dict}'


class FinditerBase(metaclass=FinditerBaseMeta):
    @property
    @abc.abstractmethod
    def pattern(self) -> AnyStr:
        pass

    flags = 0

    def __init__(self, text: str):
        self.re_compile = re.compile(pattern=self.pattern, flags=self.flags)
        self.text = text

    def __iter__(self) -> Iterator:
        self._iter = self.re_compile.finditer(string=self.text)
        return self

    def __next__(self) -> FinditerMatchObject:
        return FinditerMatchObject(match_object=next(self._iter))
