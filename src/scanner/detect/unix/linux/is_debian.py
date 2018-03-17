from scanner.transports import get_transport
from scanner.const import OS, LINUX
from scanner.detect.functions import BaseDetector, os_detect, is_os_detect


class DebianDetector(BaseDetector):
    requisites = OS.LINUX
    detection_os = LINUX.DEBIAN
    detectors = []

    def detect(self):
        transport = get_transport('unix')
        result = transport.send_command('lsb_release -i')

        if result.Output and result.Output.split('\t')[-1] == LINUX.DEBIAN:
            return True

        return False
