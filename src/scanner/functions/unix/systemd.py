from collections import OrderedDict
from configparser import ConfigParser, Error
import re
import logging

from scanner.functions.parsers import FinditerBase

LOGGER = logging.getLogger(__name__)


class MultiOrderedDictRaw(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict, self).__setitem__(key, value)

    def keys(self):
        return super(OrderedDict, self).keys()


class SystemdUnitParser:
    def __init__(self, raw):
        self._raw = raw
        self.config = ConfigParser(
            dict_type=MultiOrderedDictRaw,
            empty_lines_in_values=False,
            interpolation=None,
            strict=False
        )
        self.config.optionxform = lambda x: x
        self.result_dict = None
        self.logger = LOGGER.getChild(self.__class__.__name__)

    def _create_dict(self) -> None:
        self.result_dict = {}
        for section in self.config.sections():
            self.result_dict[section] = dict(
                self.config.items(section, raw=True)
            )

    def get_dict(self) -> dict:
        if self.result_dict is None:
            try:
                self.config.read_string(self._raw)
            except Error as e:
                self.logger.error(e.message)
                return {}

            self._create_dict()

        return self.result_dict


class SystemdUnitFiles(FinditerBase):
    pattern = r'''
        ^
        (?P<UnitName>
            (?P<Name>\S+)\.
            (?P<Type>
                automount |
                mount |
                path |
                scope |
                service |
                slice |
                socket |
                swap |
                target |
                timer
            )
        )\s+
        (?P<State>
            static  |
            generated |
            enabled |
            disabled |
            masked |
            enabled-runtime |
            transient
        )
        $
    '''

    flags = re.MULTILINE | re.VERBOSE
