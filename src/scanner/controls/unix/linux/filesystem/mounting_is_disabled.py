from scanner.const import os
from scanner.types import BaseContol, is_item_detected
from scanner.transports import get_transport
from scanner.functions.unix.lsmod_parser import LsmodParser


class Control(BaseContol, control_number=1):
    file_systems = (
        'cramfs',
        'freevxfs',
        'jffs2',
        'hfs',
        'hfsplus',
        'squashfs',
        'udf',
        'vfat',
    )

    def prerequisite(self):
        return is_item_detected(os.LINUX)

    def check(self):
        transport = get_transport('unix')
        lsmod_result = transport.send_command('lsmod')
        lsmod = [
            item.Name
            for item in LsmodParser(text=lsmod_result.Output)
        ]

        is_compliance = True
        results = []

        for fs in self.file_systems:
            if fs in lsmod:
                is_compliance = False
                results.append(f'{fs} is loaded')
                continue

            modprobe_status = transport.send_command(f'modprobe -n -v {fs}')

            if 'install /bin/true' not in modprobe_status.Output:
                is_compliance = False
                results.append(f'{fs} is not disabled')
                continue

            results.append(f'{fs} is disabled')

        result = '\n'.join(results)

        if is_compliance:
            self.control.compliance(
                result=result
            )
        else:
            self.control.not_compliance(
                result=result
            )

