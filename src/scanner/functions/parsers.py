import re
import logging
from typing import Dict, AnyStr


LOGGER = logging.getLogger(__name__)


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
