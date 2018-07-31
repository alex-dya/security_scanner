from scanner.detect.unix.linux import is_opensuse
from scanner.const import os
from scanner.const.linux import distributives
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsOpenSUSE(BaseUnixDetectTest):
    origin_module = is_opensuse
    origin_class = is_opensuse.OpensuseDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX, os.LINUX),
            text='''
            NAME="openSUSE Leap"
            VERSION="42.3"
            ID=opensuse
            ID_LIKE="suse"
            VERSION_ID="42.3"
            PRETTY_NAME="openSUSE Leap 42.3"
            ANSI_COLOR="0;32"
            CPE_NAME="cpe:/o:opensuse:leap:42.3"
            BUG_REPORT_URL="https://bugs.opensuse.org"
            HOME_URL="https://www.opensuse.org/"
            ''',
            detect_items=(distributives.OPENSUSE, )
        ),
        DetectCase(
            is_detected=(os.UNIX, os.LINUX,),
            text='''
            PRETTY_NAME="Debian GNU/Linux 9 (stretch)"
            NAME="Debian GNU/Linux"
            VERSION_ID="9"
            VERSION="9 (stretch)"
            ID=debian
            HOME_URL="https://www.debian.org/"
            SUPPORT_URL="https://www.debian.org/support"
            BUG_REPORT_URL="https://bugs.debian.org/"
            ''',
            detect_items=tuple()
        ),
        DetectCase(
            is_detected=(os.UNIX,),
            text='',
            detect_items=tuple()
        ),
    ]
