from functools import partial

import pytest

from scanner.types import ControlStatus
from scanner.controls.unix.linux.users import only_one_root


test_cases = [
    (
        ''' 
        root:x:0:0:root:/root:/bin/bash
        daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
        bin:x:2:2:bin:/bin:/usr/sbin/nologin
        sys:x:3:3:sys:/dev:/usr/sbin/nologin
        sync:x:4:65534:sync:/bin:/bin/sync
        ''',
        ControlStatus.Compliance
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
        ControlStatus.NotCompliance
    ),
]


@pytest.mark.parametrize('text,result', test_cases)
def test_cases(monkeypatch, text, result, get_transport_patch):
    monkeypatch.setattr(
        only_one_root, 'get_transport', partial(get_transport_patch, text=text))
    control = only_one_root.Control()
    monkeypatch.setattr(only_one_root, 'is_os_detect', lambda x: True)
    control.run()
    assert control.control.status == result


def test_not_applicable(monkeypatch):
    control = only_one_root.Control()
    monkeypatch.setattr(only_one_root, 'is_os_detect', lambda x: False)
    control.run()
    assert control.control.status == ControlStatus.NotApplicable
