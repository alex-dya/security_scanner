from scanner.detect.unix.linux.init_subsystem import is_systemd
from scanner.const import os
from scanner.const.linux import init_subsystem
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsSystemd(BaseUnixDetectTest):
    origin_module = is_systemd
    origin_class = is_systemd.SystemdDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX, os.LINUX,),
            text='/lib/systemd/systemd',
            detect_items=(init_subsystem.SYSTEMD,)
        ),
        DetectCase(
            is_detected=(os.UNIX, os.LINUX,),
            text='/usr/lib/systemd/systemd',
            detect_items=(init_subsystem.SYSTEMD,)
        ),
        DetectCase(
            is_detected=(os.UNIX, os.LINUX),
            text='/sbin/init',
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
