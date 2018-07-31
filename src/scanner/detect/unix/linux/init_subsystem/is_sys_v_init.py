from scanner.transports import get_transport
from scanner.const import os
from scanner.const.linux import init_subsystem
from scanner.types import BaseDetector


class SysVInitDetector(BaseDetector):
    requisites = os.LINUX
    detection_items = init_subsystem.SYS_V_INIT
    detectors = []

    def detect(self):
        transport = get_transport('unix')
        command = 'readlink -f /proc/1/exe'
        result = transport.send_command(command)

        if not result.Output:
            return False

        return result.Output == '/sbin/init'
