from scanner.detect.unix.linux.init_subsystem import is_upstart
from scanner.const import os
from scanner.const.linux import init_subsystem
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsSysVInit(BaseUnixDetectTest):
    origin_module = is_upstart
    origin_class = is_upstart.UpstartDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX, os.LINUX,),
            text='init (upstart 1.12.1)',
            detect_items=(init_subsystem.UPSTART,)
        ),
        DetectCase(
            is_detected=(os.UNIX, os.LINUX,),
            text='init something',
            detect_items=tuple()
        ),
        DetectCase(
            is_detected=(os.UNIX, os.LINUX),
            text='',
            detect_items=tuple()
        ),
        DetectCase(
            is_detected=(os.UNIX,),
            text='',
            detect_items=tuple()
        ),
    ]
