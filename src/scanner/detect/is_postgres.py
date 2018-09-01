from scanner.const import db
from scanner.transports import get_transport
from scanner.types import BaseDetector


class PostgreSQLQDetector(BaseDetector):
    requisites = None
    detection_items = db.POSTGRESQL
    detectors = []

    def detect(self):
        transport = get_transport('postgres')
        result = transport.request('SELECT version()')
        value = result[0][0]
        self.logger.debug(f'value={value!r}')
        if 'PostgreSQL' in value:
            return True

        return False
