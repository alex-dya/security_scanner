from functools import partial

import pytest

from scanner.types import BaseTransport, ControlStatus
from scanner.controls.unix.linux.users import only_one_root
from scanner.transports.ssh import ExecResult


class DummyUnixTransport(BaseTransport):
    def __init__(self, text: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._text = text

    def connect(self) -> None:
        pass

    def is_connect(self) -> bool:
        return True

    def send_command(self, text: str) -> str:
        return ExecResult(Output=self._text, ExitStatus=0)


def get_transport(name: str, text: str) -> BaseTransport:
    return DummyUnixTransport(text=text)


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
def test_cases(monkeypatch, text, result):
    monkeypatch.setattr(
        only_one_root, 'get_transport', partial(get_transport, text=text))
    control = only_one_root.Control()
    monkeypatch.setattr(control, 'prerequisite', lambda: True)
    control.run()
    assert control.control.status == result


def test_not_applicable(monkeypatch):
    control = only_one_root.Control()
    monkeypatch.setattr(control, 'prerequisite', lambda: False)
    control.run()
    assert control.control.status == ControlStatus.NotApplicable
