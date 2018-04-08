from scanner.transports import get_transport
from scanner.const import os, linux, linux_id
from scanner.types import BaseDetector
from scanner.functions.parsers import KeyValueParser


class DebianDetector(BaseDetector):
    requisites = os.LINUX
    detection_os = linux.DEBIAN
    detectors = []

    def detect(self):
        transport = get_transport('unix')
        command = 'cat /etc/os-release'
        result = transport.send_command(command)

        if result.ExitStatus != 0:
            self.logger.error(f'Wrong execution {command!r}: {result.Output}')
            return False

        if result.Output:
            os_release = KeyValueParser(text=result.Output)
            return os_release.ID == linux_id.DEBIAN

        return False
