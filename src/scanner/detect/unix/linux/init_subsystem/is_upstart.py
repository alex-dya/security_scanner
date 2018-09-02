from scanner.transports import get_transport
from scanner.const import os
from scanner.const.linux import init_subsystem
from scanner.detect.types import BaseDetector


class UpstartDetector(BaseDetector):
    requisites = os.LINUX
    detection_items = init_subsystem.UPSTART
    detectors = []

    def detect(self):
        transport = get_transport('unix')
        command = 'initctl --version'
        result = transport.send_command(command)

        if not result.Output:
            return False

        return 'upstart' in result.Output
