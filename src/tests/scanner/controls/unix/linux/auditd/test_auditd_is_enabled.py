from scanner.controls.unix.linux.auditd import auditd_is_enabled
from scanner.types import ControlStatus
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestAuditdIsEnabled(BaseUnixControlTest):
    origin = auditd_is_enabled
    case_list = [
        (
            '''
            auditd.service              enabled
            ''',
            ControlStatus.Compliance,
            '''
            auditd.service state is enabled
            '''
        ),
        (
            '''
            auditd.service              disabled
            ''',
            ControlStatus.NotCompliance,
            '''
            auditd.service state is disabled
            '''
        ),
        (
            '''
            auditd.service              disabled
            auditdata.service           enabled
            ''',
            ControlStatus.NotCompliance,
            '''
            auditd.service state is disabled
            '''
        ),
    ]
