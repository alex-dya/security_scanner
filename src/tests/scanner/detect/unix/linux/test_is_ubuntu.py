from scanner.detect.unix.linux import is_ubuntu
from scanner.const import os
from scanner.const.linux import distributives
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsUbuntu(BaseUnixDetectTest):
    origin_module = is_ubuntu
    origin_class = is_ubuntu.UbuntuDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX, os.LINUX),
            text='''
            NAME="Ubuntu"
            VERSION="18.04.1 LTS (Bionic Beaver)"
            ID=ubuntu
            ID_LIKE=debian
            PRETTY_NAME="Ubuntu 18.04.1 LTS"
            VERSION_ID="18.04"
            HOME_URL="https://www.ubuntu.com/"
            SUPPORT_URL="https://help.ubuntu.com/"
            BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
            PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
            VERSION_CODENAME=bionic
            UBUNTU_CODENAME=bionic
            ''',
            detect_items=(distributives.UBUNTU, )
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
