from scanner.detect.unix import is_solaris
from scanner.const import os
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsSolaris(BaseUnixDetectTest):
    origin_module = is_solaris
    origin_class = is_solaris.SolarisDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX,),
            text='SunOS',
            detect_items=(os.SOLARIS, )
        ),
        DetectCase(
            is_detected=(os.UNIX,),
            text='AIX',
            detect_items=tuple()
        ),
    ]
