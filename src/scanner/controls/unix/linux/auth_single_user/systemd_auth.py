from itertools import product, chain
from pathlib import PurePosixPath as Path

from scanner.const.linux import init_subsystem, systemd
from scanner.types import BaseContol, is_item_detected
from scanner.transports import get_transport
from scanner.functions.unix.systemd import SystemdUnitParser


class Control(BaseContol, control_number=8):
    files = dict(
        emergency='emergency.service',
        rescue='rescue.service',
    )

    def prerequisite(self):
        return is_item_detected(init_subsystem.SYSTEMD)

    def check(self):
        transport = get_transport('unix')
        file_contents = {}
        for file, path in product(sorted(self.files), systemd.UNIT_PATHS):
            if file in file_contents:
                continue

            result = transport.get_file_content(str(Path(path, self.files[file])))
            if result.ExitStatus != 0:
                continue

            if not result.Output:
                continue

            file_contents[file] = SystemdUnitParser(result.Output).get_dict()

        if not file_contents:
            self.control.not_compliance(
                result=f'There are not files {", ".join(self.files.values())}'
            )
            return

        errors = []
        rights_value = []

        for file, config in file_contents.items():
            file = self.files[file]
            value = config.get('Service', {}).get('ExecStart', None)
            if value is None:
                errors.append(f'{file} does not have '
                              f'"ExecStart" in section "Service"')
                continue

            right = next(
                (
                    val
                    for val in value
                    if 'systemd-sulogin-shell' in val or
                       '/sbin/sulogin' in val
                ),
                None
            )

            if right is None:
                errors.append(
                    f'{file} has wrong "ExecStart" value = "{value[0]}"')
                continue

            rights_value.append(f'{file} has right value = "{right}"')

        result = '\n'.join(chain(rights_value, errors))

        if not errors:
            self.control.compliance(
                result=result
            )
        else:
            self.control.not_compliance(
                result=result
            )
