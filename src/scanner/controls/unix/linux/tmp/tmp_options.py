from scanner.const import OS
from scanner.types import BaseContol, is_os_detect
from scanner.transports import get_transport
from scanner.functions.mount_parser import MountFinditer


class Control(BaseContol, control_number=2):
    needed_options = (
        'nodev',
        'nosuid',
        'noexec',
    )

    def prerequisite(self):
        return is_os_detect(OS.LINUX)

    def check(self):
        transport = get_transport('unix')
        result = transport.send_command('mount | grep /tmp')
        for item in MountFinditer(text=result.Output):
            if item.Path != '/tmp':
                continue

            options = [
                opt.strip()
                for opt in item.Options.split(',')
            ]

            missing_options = ','.join(
                opt
                for opt in self.needed_options
                if opt not in options
            )

            needed_options = ','.join(self.needed_options)

            if not missing_options:
                self.control.compliance(
                    result=f'/tmp has been mounted with'
                           f' options "{needed_options}"'
                )
            else:
                self.control.not_compliance(
                    result=f'/tmp has been mounted without'
                           f' options "{missing_options}"'
                )

            break
        else:
            self.control.not_compliance(
                result=f'/tmp has not been mounted on separated partition'
            )
