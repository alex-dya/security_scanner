from scanner.types import ControlStatus
from scanner.controls.postgres import log_destination
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestLogDestination(BaseUnixControlTest):
    origin = log_destination
    case_list = [
        (
            (
                [
                    ('log_destination', 'csvlog', 'description')
                ],
            ),
            ControlStatus.Compliance,
            '''
            csvlog
            '''
        ),
        (
            (
                [
                    ('log_destination', 'stderr', 'description')
                ],
            ),
            ControlStatus.NotCompliance,
            '''
            stderr
            '''
        ),
    ]
