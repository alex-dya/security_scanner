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


class BaseUnixTest(ABC):
    @property
    @abstractmethod
    def case_list(self):
        pass

    @property
    @abstractmethod
    def origin(self):
        pass

    def test_cases(self, monkeypatch, get_transport_patch):
        for item in self.case_list:
            text, status, result = item
            text = dedent(text)
            self.execute(monkeypatch, text, status, result, get_transport_patch)

    def not_applicable_prerequisite(self):
        return False

    def execute(self, monkeypatch, text, status, result, get_transport_patch):
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

    def execute_not_applicable(self, monkeypatch):
        control = self.origin.Control()
        monkeypatch.setattr(
            control, 'prerequisite', self.not_applicable_prerequisite)
        control.run()
        assert control.control.status == ControlStatus.NotApplicable
