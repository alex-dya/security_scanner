from scanner.detect import is_unix
from scanner.const import os
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsUnix(BaseUnixDetectTest):
    origin_module = is_unix
    origin_class = is_unix.UnixDetector
    case_list = [
        DetectCase(
            is_detected=tuple(),
            text='AIX',
            detect_items=(os.UNIX, )
        ),
        DetectCase(
            is_detected=tuple(),
            text='Mikrotik',
            detect_items=tuple()
        ),
    ]
