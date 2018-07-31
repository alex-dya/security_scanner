from .is_debian import DebianDetector
from .is_centos import CentosDetector
from .is_opensuse import OpensuseDetector
from .is_ubuntu import UbuntuDetector
from .init_subsystem import detectors as init_detectors

detectors = [
    DebianDetector,
    CentosDetector,
    OpensuseDetector,
    UbuntuDetector,
]

detectors.extend(init_detectors)
