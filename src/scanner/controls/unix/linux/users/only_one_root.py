from scanner.const import os
from scanner.types import BaseContol, is_os_detect
from scanner.transports import get_transport
from scanner.functions.passwd_parser import PasswdParser


class Control(BaseContol, control_number=6):
    def prerequisite(self):
        return is_os_detect(os.LINUX)

    def check(self):
        transport = get_transport('unix')
        result = transport.send_command('cat /etc/passwd')
        root_list = [
            item
            for item in PasswdParser(content=result.Output)
            if item.UID == 0
        ]

        if len(root_list) > 1:
            self.control.not_compliance(
                result=f'There are {len(root_list)} roots: {root_list}'
            )
        else:
            self.control.compliance(
                result=f'There is only one root'
            )
