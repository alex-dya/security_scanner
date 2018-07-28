from scanner.detect.unix import is_freebsd
from scanner.const import os
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsFreeBSD(BaseUnixDetectTest):
    origin_module = is_freebsd
    origin_class = is_freebsd.FreebsdDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX,),
            text='FreeBSD',
            detect_items=(os.FREEBSD, )
        ),
        DetectCase(
            is_detected=(os.UNIX,),
            text='AIX',
            detect_items=tuple()
        ),
    ]
