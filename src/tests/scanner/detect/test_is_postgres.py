from scanner.detect import is_postgres
from scanner.const import db
from tests.scanner.detect.conftest import BaseUnixDetectTest, DetectCase


class TestIsPostgres(BaseUnixDetectTest):
    origin_module = is_postgres
    origin_class = is_postgres.PostgreSQLQDetector
    case_list = [
        DetectCase(
            is_detected=tuple(),
            text=[
                [('PostgreSQL 10.4 (Debian 10.4-2.pgdg90+1) on '
                  'x86_64-pc-linux-gnu, compiled by gcc (Debian '
                  '6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit',)]
            ],
            detect_items=(db.POSTGRESQL, )
        ),
        DetectCase(
            is_detected=tuple(),
            text='',
            detect_items=tuple()
        ),
    ]
