from scanner.const import os
from scanner.const.linux import init_subsystem, systemd
from scanner.types import BaseContol, is_item_detected
from scanner.transports import get_transport
from scanner.functions.unix.systemd import SystemdUnitFiles


class Control(BaseContol, control_number=9):
    def prerequisite(self):
        return (is_item_detected(os.LINUX) and
                is_item_detected(init_subsystem.SYSTEMD))

    def check(self):
        transport = get_transport('unix')
        result = transport.send_command(
            'systemctl list-unit-files --plain --no-legend --no-pager')

        if result.ExitStatus != 0:
            self.control.not_applicable()

        service_list = [
            item
            for item in SystemdUnitFiles(result.Output)
            if item.Name == 'cron'
        ]

        if not service_list:
            self.control.not_compliance(
                result=f'There is not any cron service'
            )
            return

        cron_service = service_list[0]

        if cron_service.State != systemd.ENABLED:
            self.control.not_compliance(
                result=f'{cron_service.UnitName} state is {cron_service.State}'
            )
            return

        self.control.compliance(
            result=f'{cron_service.UnitName} state is {cron_service.State}'
        )
