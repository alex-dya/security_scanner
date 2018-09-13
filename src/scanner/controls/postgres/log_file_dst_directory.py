from scanner.controls.postgres.config_checker import SettingChecker
from scanner.controls import BaseContol


class Control(SettingChecker, BaseContol, control_number=12):
    def check_settings(self, settings):
        result = settings.get('log_directory')
        if result is None:
            result = '/'

        if result == 'logs':
            self.control.compliance(
                result=result
            )
        else:
            self.control.not_compliance(
                result=result
            )
