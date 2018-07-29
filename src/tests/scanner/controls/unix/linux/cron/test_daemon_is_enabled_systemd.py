from scanner.types import ControlStatus
from scanner.controls.unix.linux.cron import daemon_is_enabled_systemd
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestDaemonIsEnabledSystemd(BaseUnixControlTest):
    origin = daemon_is_enabled_systemd
    case_list = [
        (
            '''
            anacron.service             enabled
            cron.service                enabled
            ''',
            ControlStatus.Compliance,
            '''
            cron.service state is enabled
            '''
        ),
        (
            '''
            anacron.service             enabled
            cron.service                disabled
            ''',
            ControlStatus.NotCompliance,
            '''
            cron.service state is disabled
            '''
        ),
        (
            '''
            anacron.service             enabled
            ''',
            ControlStatus.NotCompliance,
            '''
            There is not any cron service
            '''
        ),
    ]
