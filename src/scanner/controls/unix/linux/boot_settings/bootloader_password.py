from scanner.const import os
from scanner.types import BaseContol, is_item_detected
from scanner.transports import get_transport


class Control(BaseContol, control_number=7):
    file_paths = (
        '/boot/grub/menu.lst',
        '/boot/grub2/menu.lst',
        '/boot/grub/grub.cfg',
        '/boot/grub2/grub.cfg',
        '/boot/grub/grub.conf',
        '/boot/grub2/grub.conf',
        '/etc/grub.conf'
    )

    password_strings = (
        'set superuser',
        'password'
    )

    def prerequisite(self):
        return is_item_detected(os.LINUX)

    def check(self):
        transport = get_transport('unix')

        boot_configs = {}
        for file in self.file_paths:
            result = transport.get_file_content(file)
            if result.ExitStatus != 0:
                continue

            boot_configs[file] = result.Output

        if not boot_configs:
            self.control.not_applicable()

        is_compliance = False
        results = []

        for file_name, content in boot_configs.items():
            if not content:
                continue

            lines = [
                f'{file_name}:{number}:{line}'
                for number, line in enumerate(
                    map(str.strip, content.splitlines()),
                    1
                )
                if line.startswith(self.password_strings)
            ]

            if not lines:
                continue

            results.extend(lines)
            is_compliance = True

        result = '\n'.join(results)

        if is_compliance:
            self.control.compliance(
                result=result
            )
        else:
            self.control.not_compliance(
                result='The password is not set up'
            )
