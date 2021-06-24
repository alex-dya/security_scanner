from scanner.const import os
from scanner.const.linux import init_subsystem, systemd
from scanner.functions.unix.systemd import SystemdUnitFiles
from scanner.transports import get_transport
from scanner.types import BaseContol, is_item_detected


class Control(BaseContol, control_number=11):
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
            if item.Name == 'auditd'
        ]

        if not service_list:
            self.control.not_compliance(
                result=f'There is not any auditd service'
            )
            return

        auditd_service = service_list[0]

        if auditd_service.State != systemd.ENABLED:
            self.control.not_compliance(
                result=f'{auditd_service.UnitName} state is {auditd_service.State}'
            )
            return

        self.control.compliance(
            result=f'{auditd_service.UnitName} state is {auditd_service.State}'
        )
