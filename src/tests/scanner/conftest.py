import logging
from typing import Callable, Tuple, List
from os import devnull

import pytest

from scanner.transports.ssh import ExecResult
from scanner.types import BaseTransport

logging.basicConfig(stream=open(devnull, 'w'))


class DummyUnixTransport(BaseTransport):
    def __init__(self, data: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._text = iter(data)

    def connect(self) -> None:
        pass

    def is_connect(self) -> bool:
        return True

    def disconnect(self):
        pass

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


class DummyPostgresTransport(BaseTransport):
    def __init__(self, data: List[List[Tuple]], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = iter(data)

    def connect(self) -> None:
        pass

    @property
    def is_connect(self) -> bool:
        pass

    def disconnect(self) -> None:
        pass

    def request(self, request: str):
        output = next(self.data, None)

        if output is None:
            raise ExpectedCommandError(f'Expected request({request})')

        return output


def get_transport(name, **kwargs) -> BaseTransport:
    if name in ('unix', 'ssh'):
        return DummyUnixTransport(**kwargs)

    if name == 'postgres':
        return DummyPostgresTransport(**kwargs)


class ExpectedCommandError(Exception):
    pass


@pytest.fixture(scope='module')
def get_transport_patch() -> Callable:
    return get_transport
