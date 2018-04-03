from scanner.const import OS
from scanner.types import BaseContol, is_os_detect
from scanner.transports import get_transport
from scanner.functions.mount_parser import MountFinditer


class Control(BaseContol, control_number=1):
    def prerequisite(self):
        return is_os_detect(OS.LINUX)

    def check(self):
        transport = get_transport('unix')
        result = transport.send_command('mount | grep /tmp')
        for item in MountFinditer(text=result.Output):
            self.control.compliance(result=f'/tmp has been mount on {item.Device}')
            break
        else:
            self.control.not_compliance(result=f'/tmp has not separate partition')
