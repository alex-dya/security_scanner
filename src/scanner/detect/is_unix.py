from scanner.const import os
from scanner.mappings import unameOS
from scanner.transports import get_transport
from scanner.detect.types import BaseDetector
from .unix import detectors


class UnixDetector(BaseDetector):
    requisites = None
    detection_items = os.UNIX
    detectors = detectors

    def detect(self):
        transport = get_transport('ssh')
        result = transport.send_command('uname -s')

        if result.ExitStatus != 0:
            return False

        if result.Output and unameOS(result.Output) is not None:
            return True

        return False
