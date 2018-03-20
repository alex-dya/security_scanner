from .is_linux import LinuxDetector
from .is_solaris import SolarisDetector
from .is_freebsd import FreebsdDetector


detectors = [
    LinuxDetector(),
    SolarisDetector(),
    FreebsdDetector()
]
