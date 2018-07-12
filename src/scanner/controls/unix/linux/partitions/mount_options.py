from scanner.const import os, mount
from scanner.types import BaseContol, is_os_detect, ControlStatus
from scanner.transports import get_transport
from scanner.functions.mount_parser import MountFinditer


class Control(BaseContol, control_number=4):
    partitions = {
        '/var/tmp': (
            mount.NODEV,
            mount.NOSUID,
            mount.NOEXEC,
        ),
        '/home': (
            mount.NODEV,
        ),
        '/dev/shm': (
            mount.NODEV,
            mount.NOSUID,
            mount.NOEXEC,
        )
    }

    def prerequisite(self):
        return is_os_detect(os.LINUX)

    def check(self):
        transport = get_transport('unix')
        result = transport.send_command('mount')

        separated = {
            item.Path: item.Options
            for item in MountFinditer(text=result.Output)
            if item.Path in self.partitions
        }

        results = []
        status = ControlStatus.Compliance

        for path, options in self.partitions.items():
            if path not in separated:
                status = ControlStatus.NotCompliance
                results.append(
                    f'{path} has not been mounted on separated partition'
                )
                continue

            missing_options = ','.join(
                opt
                for opt in options
                if opt not in separated[path]
            )

            needed_options = ','.join(options)

            if not missing_options:
                results.append(
                    f'{path} has been mounted with options "{needed_options}"'
                )
            else:
                status = ControlStatus.NotCompliance
                results.append(
                    f'{path} has been mounted without options "{missing_options}"'
                )

        self.control.result = '\n'.join(results)
        self.control.status = status
