from .is_sys_v_init import SysVInitDetector
from .is_upstart import UpstartDetector
from .is_systemd import SystemdDetector

detectors = [
    UpstartDetector,
    SysVInitDetector,
    SystemdDetector
]
