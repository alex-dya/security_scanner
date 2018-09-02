from scanner.controls.types import ControlStatus
from scanner.controls.unix.linux.auth_single_user import sysvinit_auth
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestSysVInitAuth(BaseUnixControlTest):
    origin = sysvinit_auth
    case_list = [
        (
            (
                'root:x:0:0:root:/root:/bin/bash',
                'root:$6$PghlV1iR$0AH1r8TwJfcBuHjqTyhSS3K30:17601:0:99999:7:::',
                '''
                # Boot to X11
                id:5:initdefault:
                
                rc::sysinit:/etc/rc.sysinit
                rs:S1:wait:/etc/rc.single
                s51:S:respawn:/sbin/sulogin
                ''',
                '''
                # terminal sequence to reset to the default color.
                SETCOLOR_NORMAL="echo -en \\033[0;39m"
                SINGLE=/sbin/sulogin
                ''',
            ),
            ControlStatus.Compliance,
            '''
            Single user mode is protected with password
            '''
        ),
        (
            (
                'root:$01fasdf:0:0:root:/root:/bin/bash',
                '',
                '''
                # Boot to X11
                id:5:initdefault:
                
                rc::sysinit:/etc/rc.sysinit
                rs:S1:wait:/etc/rc.single
                s51:S:respawn:/sbin/sulogin
                ''',
                '''
                # terminal sequence to reset to the default color.
                SETCOLOR_NORMAL="echo -en \\033[0;39m"
                SINGLE=/sbin/sulogin
                ''',
            ),
            ControlStatus.Compliance,
            '''
            Single user mode is protected with password
            '''
        ),
        (
            (
                'root:x:0:0:root:/root:/bin/bash',
                '',
                '''
                # Boot to X11
                id:5:initdefault:
    
                rc::sysinit:/etc/rc.sysinit
                rs:S1:wait:/etc/rc.single
                s51:S:respawn:/sbin/sulogin
                ''',
                '''
                # terminal sequence to reset to the default color.
                SETCOLOR_NORMAL="echo -en \\033[0;39m"
                SINGLE=/sbin/sulogin
                ''',
            ),
            ControlStatus.NotCompliance,
            '''
            User root does not have password
            '''
        ),
        (
            (
                'root:x:0:0:root:/root:/bin/bash',
                'root:$6$PghlV1iR$0AH1r8TwJfcBuHjqTyhSS3K30:17601:0:99999:7:::',
                '''
                # Boot to X11
                id:5:initdefault:
    
                rc::sysinit:/etc/rc.sysinit
                rs:S1:wait:/etc/rc.single
                ''',
                '''
                # terminal sequence to reset to the default color.
                SETCOLOR_NORMAL="echo -en \\033[0;39m"
                SINGLE=/sbin/sulogin
                ''',
            ),
            ControlStatus.NotCompliance,
            '''
            Inittab does not have correct line
            '''
        ),
        (
            (
                'root:x:0:0:root:/root:/bin/bash',
                'root:$6$PghlV1iR$0AH1r8TwJfcBuHjqTyhSS3K30:17601:0:99999:7:::',
                '''
                # Boot to X11
                id:5:initdefault:
    
                rc::sysinit:/etc/rc.sysinit
                rs:S1:wait:/etc/rc.single
                s51:S:respawn:/sbin/sulogin
                ''',
                '''
                # terminal sequence to reset to the default color.
                SETCOLOR_NORMAL="echo -en \\033[0;39m"
                ''',
            ),
            ControlStatus.NotCompliance,
            '''
            /etc/sysconfig/init does not have right attribute SINGLE
            '''
        ),
        (
            (
                'root:x:0:0:root:/root:/bin/bash',
                'root:x:17601:0:99999:7:::',
                '''
                # Boot to X11
                id:5:initdefault:
    
                rc::sysinit:/etc/rc.sysinit
                rs:S1:wait:/etc/rc.single
                ''',
                '''
                # terminal sequence to reset to the default color.
                SETCOLOR_NORMAL="echo -en \\033[0;39m"
                ''',
            ),
            ControlStatus.NotCompliance,
            '''
            User root does not have password
            Inittab does not have correct line
            /etc/sysconfig/init does not have right attribute SINGLE
            '''
        ),
    ]
