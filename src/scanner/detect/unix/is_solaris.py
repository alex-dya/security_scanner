from scanner.transports import get_transport
from scanner.mappings import unameOS
from scanner.const import os
from scanner.types import BaseDetector


class SolarisDetector(BaseDetector):
    requisites = os.UNIX
    detection_os = os.SOLARIS
    detectors = []

    def detect(self):
        transport = get_transport('unix')
        command = 'uname -s'
        result = transport.send_command(command)

        if result.ExitStatus != 0:
            self.logger.error(f'Wrong execution {command!r}: {result.Output}')
            return False

        if result.Output and unameOS(result.Output) == os.SOLARIS:
            return True

        return False
