from scanner.detect.unix import is_linux
from scanner.const import os
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsLinux(BaseUnixDetectTest):
    origin_module = is_linux
    origin_class = is_linux.LinuxDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX,),
            text='Linux',
            detect_items=(os.LINUX, )
        ),
        DetectCase(
            is_detected=(os.UNIX,),
            text='FreeBSD',
            detect_items=tuple()
        ),
    ]
