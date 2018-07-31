from scanner.types import ControlStatus
from scanner.controls.unix.linux.boot_settings \
    import permissions_on_bootloader_config
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestPermissionsOnBootloaderConfig(BaseUnixControlTest):
    origin = permissions_on_bootloader_config
    case_list = [
        (
            ''' 
            stat: cannot stat '/boot/grub/menu.lst': No such file or directory
            stat: cannot stat '/boot/grub2/menu.lst': No such file or directory
            stat: cannot stat '/boot/grub/grub.cfg': No such file or directory
            regular file|600|root|root|9474|1531771694|/boot/grub2/grub.cfg
            stat: cannot stat '/boot/grub/grub.conf': No such file or directory
            stat: cannot stat '/boot/grub2/grub.conf': No such file or directory
            stat: cannot stat '/etc/grub.conf': No such file or directory
            ''',

            ControlStatus.Compliance,
            '''
            /boot/grub2/grub.cfg root:root 600
            '''
        ),
        (
            ''' 
            regular file|666|root|root|9474|1531771694|/boot/grub2/grub.cfg
            ''',

            ControlStatus.NotCompliance,
            '''
            /boot/grub2/grub.cfg root:root 666
            '''
        ),
        (
            ''' 
            regular file|600|vmuser|root|9474|1531771694|/boot/grub2/grub.cfg
            ''',

            ControlStatus.NotCompliance,
            '''
            /boot/grub2/grub.cfg vmuser:root 600
            '''
        ),
        (
            ''' 
            regular file|600|root|vmgroup|9474|1531771694|/boot/grub2/grub.cfg
            ''',

            ControlStatus.NotCompliance,
            '''
            /boot/grub2/grub.cfg root:vmgroup 600
            '''
        ),
        (
            ''' 
            symbolic link|600|root|vmgroup|9474|1531771694|/boot/grub2/grub.cfg
            ''',

            ControlStatus.NotApplicable,
            None
        ),
    ]
