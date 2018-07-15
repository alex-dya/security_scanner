from abc import ABC, abstractmethod
from functools import partial
from typing import Callable
from textwrap import dedent

import pytest

from scanner.types import BaseTransport, ControlStatus
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


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ != 'test_case':
        return metafunc

    idlist = [
        f'Test case {i+1}'
        for i in range(len(metafunc.cls.case_list))
    ]

    argnames = ['text', 'status', 'result']

    argvalues = [
        (dedent(scenario[0]), scenario[1], dedent(scenario[2]).strip())
        for scenario in metafunc.cls.case_list
    ]

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

    def not_applicable_prerequisite(self):
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

    def test_execute_not_applicable(self, monkeypatch):
        control = self.origin.Control()
        monkeypatch.setattr(
            control, 'prerequisite', self.not_applicable_prerequisite)
        control.run()
        assert control.control.status == ControlStatus.NotApplicable
