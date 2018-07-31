from scanner.detect.unix.linux.init_subsystem import is_sys_v_init
from scanner.const import os
from scanner.const.linux import init_subsystem
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsSysVInit(BaseUnixDetectTest):
    origin_module = is_sys_v_init
    origin_class = is_sys_v_init.SysVInitDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX, os.LINUX,),
            text='/sbin/init',
            detect_items=(init_subsystem.SYS_V_INIT,)
        ),
        DetectCase(
            is_detected=(os.UNIX, os.LINUX,),
            text='/usr/lib/systemd/systemd',
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
