from scanner.const import os
from scanner.types import BaseContol, is_item_detected
from scanner.transports import get_transport
from scanner.functions.unix.passwd_parser import PasswdParser


class Control(BaseContol, control_number=10):
    def prerequisite(self):
        return is_item_detected(os.LINUX)

    def check(self):
        transport = get_transport('unix')
        result = transport.get_file_content('/etc/passwd')
        uid_list = [
            item.Name
            for item in PasswdParser(content=result.Output)
            if item.UID < 1000 and item.Name not in ['root', 'sync', 'shutdown',
                                                     'halt'] and item.Shell != '/usr/sbin/nologin'

        ]
        if len(uid_list) > 0:
            self.control.not_compliance(
                result=f'{len(uid_list)} system accounts are not protected: {",".join(uid_list)}'
            )
            return

        self.control.compliance(
            result=f'System accounts are secured'
        )
