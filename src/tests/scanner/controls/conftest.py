from abc import ABC, abstractmethod
from functools import partial
from typing import Callable
from textwrap import dedent

import pytest

from scanner.types import BaseTransport, ControlStatus
from scanner.transports.ssh import ExecResult


class ExpectedCommandError(Exception):
    pass


class DummyUnixTransport(BaseTransport):
    def __init__(self, text: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._text = iter(text)

    def connect(self) -> None:
        pass

    def is_connect(self) -> bool:
        return True

    def send_command(self, text: str) -> ExecResult:
        try:
            return ExecResult(Output=next(self._text), Error='', ExitStatus=0)
        except StopIteration:
            raise ExpectedCommandError(f'Expected send_command({text})')

    def get_file_content(self, filename: str) -> ExecResult:
        return self.send_command(f'cat {filename}')

    def stat_file(self, filename: str) -> ExecResult:
        return self.send_command(
            f"stat -c '%F|%a|%U|%G|%s|%Y|%n' {filename}")


def get_transport(name, **kwargs) -> BaseTransport:
    if name == 'unix':
        return DummyUnixTransport(**kwargs)


@pytest.fixture(scope='module')
def get_transport_patch() -> Callable:
    return get_transport


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ != 'test_case':
        return metafunc

    idlist = [
        f'Test case {i+1}'
        for i in range(len(metafunc.cls.case_list))
    ]

    argnames = ['text', 'status', 'result']
    argvalues = []

    for text, status, result in metafunc.cls.case_list:
        if isinstance(text, str):
            text = (dedent(text),)
        else:
            text = tuple(dedent(item) for item in text)

        argvalues.append((text, status, result and dedent(result).strip()))

    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


class BaseUnixTest(ABC):
    @property
    @abstractmethod
    def case_list(self):
        pass

    @property
    @abstractmethod
    def origin(self):
        pass

    def not_passed_prerequisite(self):
        return False

    def test_case(self, monkeypatch, text, status, result, get_transport_patch):
        monkeypatch.setattr(
            self.origin,
            'get_transport',
            partial(get_transport_patch, text=text)
        )
        monkeypatch.setattr(
            self.origin.Control, 'prerequisite', lambda self_: True)
        control = self.origin.Control()
        control.run()
        assert control.control.status == status
        assert control.result == result

    def test_execute_not_checked(self, monkeypatch):
        control = self.origin.Control()
        monkeypatch.setattr(
            control, 'prerequisite', self.not_passed_prerequisite)
        control.run()
        assert control.control.status == ControlStatus.NotChecked
