from scanner.const import OS
from scanner.types import BaseContol, is_os_detect
from scanner.transports import get_transport


class Control(BaseContol, number=1):
    def prerequisite(self):
        return is_os_detect(OS.LINUX)

    def check(self):
        transport = get_transport('unix')
        result = transport.send_command('mount | grep tmp')
        self.logger.debug(result)
