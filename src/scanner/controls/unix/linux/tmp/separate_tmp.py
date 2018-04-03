from scanner.const import OS
from scanner.types import BaseContol, is_os_detect
from scanner.transports import get_transport
from scanner.functions.mount_parser import MountFinditer


class Control(BaseContol, control_number=1):
    def prerequisite(self):
        return is_os_detect(OS.LINUX)

    def check(self):
        transport = get_transport('unix')
        result = transport.send_command('mount')
        for item in MountFinditer(text=result.Output):
            if item.Path != '/tmp':
                continue

            self.control.compliance(
                result=f'/tmp has been mounted on {item.Device}'
            )
            break
        else:
            self.control.not_compliance(
                result='/tmp has not been mounted on separated partition'
            )
