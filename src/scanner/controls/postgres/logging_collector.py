from scanner.const import db
from scanner.types import BaseContol, is_item_detected
from scanner.transports import get_transport


class Control(BaseContol, control_number=11):
    def prerequisite(self):
        return is_item_detected(db.POSTGRESQL)

    def check(self):
        transport = get_transport('postgres')

        data = transport.request('show all;')
        if not data:
            self.control.not_applicable(result='Configurations is not found')
            return

        configs = {
            item[0]: item[1]
            for item in data
        }

        result = configs.get('logging_collector')

        if result is not None and result == 'on':
            self.control.compliance(
                result=result
            )
        else:
            self.control.not_compliance(
                result=result
            )
