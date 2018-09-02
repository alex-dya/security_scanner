from abc import ABCMeta, abstractmethod

from scanner.const import db
from scanner.detect.types import is_item_detected


class SettingChecker(metaclass=ABCMeta):
    def prerequisite(self):
        return is_item_detected(db.POSTGRESQL)

    def check(self):
        transport = self.get_transport('postgres')

        data = transport.request('show all;')
        if not data:
            self.control.not_applicable(result='Configurations is not found')
            return

        config = {
            item[0]: item[1]
            for item in data
        }

        self.check_settings(config)

    @abstractmethod
    def check_settings(self, settings):
        pass
