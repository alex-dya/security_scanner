from scanner.types import ControlStatus
from scanner.controls.postgres import logging_collector
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestLoggingCollector(BaseUnixControlTest):
    origin = logging_collector
    case_list = [
        (
            (
                [
                    ('logging_collector', 'on', 'description')
                ],
            ),
            ControlStatus.Compliance,
            '''
            on
            '''
        ),
        (
            (
                [
                    ('logging_collector', 'off', 'description')
                ],
            ),
            ControlStatus.NotCompliance,
            '''
            off
            '''
        ),
    ]
