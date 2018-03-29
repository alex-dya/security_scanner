import re
import logging
import abc
import re
from typing import Dict, AnyStr
from utility import AddLoggerMeta


LOGGER = logging.getLogger(__name__)


class FinditerBaseMeta(abc.ABCMeta, AddLoggerMeta):
    pass


class KeyValueParser:
    double_quotes = re.compile(r'^".+"$')

    def __init__(self, delimiter: str = '='):
        self.delimiter = delimiter
        self.result = dict()
        self.logger = LOGGER.getChild('KeyValueParser')

    def parse(self, data: str) -> Dict[AnyStr, AnyStr]:
        for line in data.splitlines():

            if not line.strip():
                continue

            key, value = map(str.strip, line.split(self.delimiter))

            if self.double_quotes.match(value):
                value = value[1:-1]

            if key in self.result:
                if isinstance(self.result[key], list):
                    self.result[key] = self.result[key] + [value]
                else:
                    self.result[key] = [self.result[key]] + [value]
            else:
                self.result[key] = value
        return self.result


class FinditerMatchObject(metaclass=AddLoggerMeta):
    def __init__(self, match_object: re.match):
        self.match = match_object
        self.dict = match_object.groupdict()

    def __getattr__(self, item):
        if item in self.dict:
            return self.dict[item]
        else:
            raise AttributeError

    def __str__(self):
        return f'{self.dict}'


class FinditerBase(metaclass=FinditerBaseMeta):
    @property
    @abc.abstractmethod
    def pattern(self):
        pass

    flags = 0

    def __init__(self):
        self.re_compile = re.compile(pattern=self.pattern, flags=self.flags)

    def __call__(self, text: str):
        for match in self.re_compile.finditer(string=text):
            yield FinditerMatchObject(match_object=match)

