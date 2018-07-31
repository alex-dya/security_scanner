import logging
from typing import Callable
from os import devnull

import pytest

from scanner.transports.ssh import ExecResult
from scanner.types import BaseTransport


logging.basicConfig(stream=open(devnull, 'w'))


class DummyUnixTransport(BaseTransport):
    def __init__(self, text: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._text = iter(text)

    def connect(self) -> None:
        pass

    def is_connect(self) -> bool:
        return True

    def send_command(self, text: str) -> ExecResult:
        output = next(self._text, None)

        if output is None:
            raise ExpectedCommandError(f'Expected send_command({text})')

        return ExecResult(Output=output, Error='', ExitStatus=0)

    def get_file_content(self, filename: str) -> ExecResult:
        return self.send_command(f'cat {filename}')

    def stat_file(self, filename: str) -> ExecResult:
        return self.send_command(
            f"stat -c '%F|%a|%U|%G|%s|%Y|%n' {filename}")


def get_transport(name, **kwargs) -> BaseTransport:
    if name == 'unix':
        return DummyUnixTransport(**kwargs)


class ExpectedCommandError(Exception):
    pass


@pytest.fixture(scope='module')
def get_transport_patch() -> Callable:
    return get_transport
