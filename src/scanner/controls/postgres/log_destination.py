from scanner.controls.postgres.config_checker import SettingChecker
from scanner.controls import BaseContol


class Control(SettingChecker, BaseContol, control_number=10):
    def check_settings(self, settings):
        result = settings.get('log_destination')

        if result is not None and result != 'stderr':
            self.control.compliance(
                result=result
            )
        else:
            self.control.not_compliance(
                result=result
            )
