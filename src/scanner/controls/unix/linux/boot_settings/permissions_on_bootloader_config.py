from operator import attrgetter
from shlex import quote

from scanner.const import os, file_type
from scanner.controls import BaseContol
from scanner.detect.types import is_item_detected
from scanner.functions.unix.stats_parser import StatsParser


class Control(BaseContol, control_number=2):
    file_paths = [
        '/boot/grub/menu.lst',
        '/boot/grub2/menu.lst',
        '/boot/grub/grub.cfg',
        '/boot/grub2/grub.cfg',
        '/boot/grub/grub.conf',
        '/boot/grub2/grub.conf',
        '/etc/grub.conf'
    ]

    def prerequisite(self):
        return is_item_detected(os.LINUX)

    def check(self):
        transport = self.get_transport('unix')
        stat_result = transport.stat_file(' '.join(map(quote, self.file_paths)))

        is_compliance = True
        results = []

        for item in sorted(
                StatsParser(stat_result.Output),
                key=attrgetter('Name')):

            if item.Type != file_type.FILE:
                continue

            results.append(
                f'{item.Name} {item.Owner}:{item.GroupOwner} '
                f'{item.Permissions:o}')

            if item.Permissions != 0o600:
                is_compliance = False

            if item.Owner != 'root':
                is_compliance = False

            if item.GroupOwner != 'root':
                is_compliance = False

        result = '\n'.join(results)

        if not result:
            self.control.not_applicable()
            return

        if is_compliance:
            self.control.compliance(
                result=result
            )
        else:
            self.control.not_compliance(
                result=result
            )

