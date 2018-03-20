from .is_debian import DebianDetector
from .is_centos import CentosDetector
from .is_opensuse import OpensuseDetector
from .is_ubuntu import UbuntuDetector

detectors = [
    DebianDetector(),
    CentosDetector(),
    OpensuseDetector(),
    UbuntuDetector()
]
