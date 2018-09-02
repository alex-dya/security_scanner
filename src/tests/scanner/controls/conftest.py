from abc import ABC, abstractmethod
from functools import partial
from textwrap import dedent

from scanner import transports
from scanner.controls.types import ControlStatus


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ != 'test_case':
        return metafunc

    idlist = [
        f'Test case {i+1}'
        for i in range(len(metafunc.cls.case_list))
    ]

    argnames = ['data', 'status', 'result']
    argvalues = []

    for data, status, result in metafunc.cls.case_list:
        if isinstance(data, str):
            data = (dedent(data),)
        elif isinstance(data[0], str):
            data = tuple(dedent(item) for item in data)

        argvalues.append((data, status, result and dedent(result).strip()))

    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


class BaseUnixControlTest(ABC):
    @property
    @abstractmethod
    def case_list(self):
        pass

    @property
    @abstractmethod
    def origin(self):
        pass

    @staticmethod
    def not_passed_prerequisite():
        return False

    def test_case(self, monkeypatch, data, status, result, get_transport_patch):
        monkeypatch.setattr(
            self.origin.Control,
            'get_transport',
            partial(get_transport_patch, data=data)
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
