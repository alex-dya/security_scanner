from scanner.controls.unix.linux.users import system_accounts_secured
from scanner.types import ControlStatus
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestSystemAccountsSecured(BaseUnixControlTest):
    origin = system_accounts_secured
    case_list = [
        (
            ''' 
            root:x:0:0:root:/root:/bin/bash
            daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
            bin:x:2:2:bin:/bin:/usr/sbin/nologin
            sys:x:3:3:sys:/dev:/usr/sbin/nologin
            sync:x:4:65534:sync:/bin:/bin/sync
            tcpdump:x:108:115::/nonexistent:/usr/sbin/nologin
            ''',
            ControlStatus.Compliance,
            'System accounts are secured'
        ),
        (
            ''' 
            root:x:0:0:root:/root:/bin/bash
            debian-tor:x:127:134::/var/lib/tor:/bin/false
            daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
            bin:x:2:2:bin:/bin:/usr/sbin/nologin
            sys:x:3:3:sys:/dev:/usr/sbin/nologin
            sync:x:4:65534:sync:/bin:/bin/sync
            ''',
            ControlStatus.NotCompliance,
            "1 system accounts are not protected: debian-tor"
        ),
    ]
