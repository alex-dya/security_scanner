from scanner.types import ControlStatus
from scanner.controls.unix.linux.users import only_one_root
from tests.scanner.controls.conftest import BaseUnixTest


class TestCase(BaseUnixTest):
    origin = only_one_root
    case_list = [
        (
            ''' 
            root:x:0:0:root:/root:/bin/bash
            daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
            bin:x:2:2:bin:/bin:/usr/sbin/nologin
            sys:x:3:3:sys:/dev:/usr/sbin/nologin
            sync:x:4:65534:sync:/bin:/bin/sync
            ''',
            ControlStatus.Compliance,
            'There is only one root'
        ),
        (
            ''' 
            root:x:0:0:root:/root:/bin/bash
            toor:x:0:0:toor:/toor:/bin/bash
            daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
            bin:x:2:2:bin:/bin:/usr/sbin/nologin
            sys:x:3:3:sys:/dev:/usr/sbin/nologin
            sync:x:4:65534:sync:/bin:/bin/sync
            ''',
            ControlStatus.NotCompliance,
            "There are 2 roots: ['root', 'toor']"
        ),
    ]
