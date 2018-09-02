from scanner.transports import get_transport
from scanner.const import os
from scanner.const.linux import linux_id, distributives
from scanner.detect.types import BaseDetector
from scanner.functions.parsers import KeyValueParser


class CentosDetector(BaseDetector):
    requisites = os.LINUX
    detection_items = distributives.CENTOS
    detectors = []

    def detect(self):
        transport = get_transport('unix')
        result = transport.get_file_content('/etc/os-release')

        if not result.Output:
            return False

        os_release = KeyValueParser(text=result.Output)
        return os_release.ID == linux_id.CENTOS
