from typing import Callable
import pytest

from scanner.types import BaseTransport
from scanner.transports.ssh import ExecResult


class DummyUnixTransport(BaseTransport):
    def __init__(self, text: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._text = text

    def connect(self) -> None:
        pass

    def is_connect(self) -> bool:
        return True

    def send_command(self, text: str) -> ExecResult:
        return ExecResult(Output=self._text, ExitStatus=0)


def get_transport(name, **kwargs) -> BaseTransport:
    if name == 'unix':
        return DummyUnixTransport(**kwargs)


@pytest.fixture(scope='module')
def get_transport_patch() -> Callable:
    return get_transport
