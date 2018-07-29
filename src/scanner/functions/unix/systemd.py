from collections import OrderedDict
from configparser import ConfigParser


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
        self.config.read_string(self._raw)
        self.result_dict = None

    def _create_dict(self) -> None:
        self.result_dict = {}
        for section in self.config.sections():
            self.result_dict[section] = dict(
                self.config.items(section, raw=True)
            )

    def get_dict(self) -> dict:
        if self.result_dict is None:
            self._create_dict()

        return self.result_dict
