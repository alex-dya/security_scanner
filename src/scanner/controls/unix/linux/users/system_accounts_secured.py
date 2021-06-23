from scanner.const import os
from scanner.functions.unix.passwd_parser import PasswdParser
from scanner.transports import get_transport
from scanner.types import BaseContol, is_item_detected


class Control(BaseContol, control_number=10):
    def prerequisite(self):
        return is_item_detected(os.LINUX)

    def check(self):
        transport = get_transport('unix')
        result = transport.get_file_content('/etc/passwd')
        user_list = [
            item.Name
            for item in PasswdParser(content=result.Output)
            if item.UID < 1000
            if item.Name not in ['root', 'sync', 'shutdown', 'halt']
            if item.Shell != '/usr/sbin/nologin'

        ]
        if len(user_list) > 0:
            self.control.not_compliance(
                result=f'{len(user_list)} system accounts are not protected: {",".join(user_list)}'
            )
            return

        self.control.compliance(
            result=f'System accounts are secured'
        )
