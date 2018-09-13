from scanner.controls.types import ControlStatus
from scanner.controls.postgres import log_file_dst_directory
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestLogDestination(BaseUnixControlTest):
    origin = log_file_dst_directory
    case_list = [
        (
            (
                [
                    ('log_directory', 'logs', 'description')
                ],
            ),
            ControlStatus.Compliance,
            '''
            logs
            '''
        ),
        (
            (
                [
                    ('log_directory', '/', 'description')
                ],
            ),
            ControlStatus.NotCompliance,
            '''
            /
            '''
        ),
        (
            (
                [
                    ('log_directory', None, 'description')
                ],
            ),
            ControlStatus.NotCompliance,
            '''
            /
            '''
        ),
    ]
