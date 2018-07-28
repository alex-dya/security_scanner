from scanner.detect.unix.linux import is_centos
from scanner.const import os
from scanner.const.linux import distributives
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsCentos(BaseUnixDetectTest):
    origin_module = is_centos
    origin_class = is_centos.CentosDetector
    case_list = [
        DetectCase(
            is_detected=(os.UNIX, os.LINUX,),
            text='''
            NAME="CentOS Linux"
            VERSION="7 (Core)"
            ID="centos"
            ID_LIKE="rhel fedora"
            VERSION_ID="7"
            PRETTY_NAME="CentOS Linux 7 (Core)"
            ANSI_COLOR="0;31"
            CPE_NAME="cpe:/o:centos:centos:7"
            HOME_URL="https://www.centos.org/"
            BUG_REPORT_URL="https://bugs.centos.org/"

            CENTOS_MANTISBT_PROJECT="CentOS-7"
            CENTOS_MANTISBT_PROJECT_VERSION="7"
            REDHAT_SUPPORT_PRODUCT="centos"
            REDHAT_SUPPORT_PRODUCT_VERSION="7"
            ''',
            detect_items=(distributives.CENTOS, )
        ),
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
            detect_items=tuple()
        ),
        DetectCase(
            is_detected=(os.UNIX,),
            text='',
            detect_items=tuple()
        ),
    ]
