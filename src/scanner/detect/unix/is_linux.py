from scanner.transports import get_transport
from scanner.mappings import unameOS
from scanner.const import OS
from scanner.detect.functions import BaseDetector
from .linux import detectors


class LinuxDetector(BaseDetector):
    requisites = OS.UNIX
    detection_os = OS.LINUX
    detectors = detectors

    def detect(self):
        transport = get_transport('unix')
        result = transport.send_command('uname -s')

        if result.Output and unameOS(result.Output) == OS.LINUX:
            return True

        return False
