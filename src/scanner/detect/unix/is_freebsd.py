from scanner.transports import get_transport
from scanner.mappings import unameOS
from scanner.const import OS
from scanner.types import BaseDetector


class FreebsdDetector(BaseDetector):
    requisites = OS.UNIX
    detection_os = OS.FREEBSD
    detectors = []

    def detect(self):
        transport = get_transport('unix')
        command = 'uname -s'
        result = transport.send_command(command)

        if result.ExitStatus != 0:
            self.logger.error(f'Wrong execution {command!r}: {result.Output}')
            return False

        if result.Output and unameOS(result.Output) == OS.FREEBSD:
            return True

        return False
