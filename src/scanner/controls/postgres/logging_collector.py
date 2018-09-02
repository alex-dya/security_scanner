from scanner.controls.postgres.config_checker import SettingChecker
from scanner.controls import BaseContol


class Control(SettingChecker, BaseContol, control_number=11):
    def check_settings(self, settings):
        result = settings.get('logging_collector')

        if result is not None and result == 'on':
            self.control.compliance(
                result=result
            )
        else:
            self.control.not_compliance(
                result=result
            )
