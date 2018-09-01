from abc import ABC, abstractmethod
from functools import partial
from textwrap import dedent
from typing import NamedTuple, Union, Iterable, AnyStr

from scanner import types


class DetectCase(NamedTuple):
    is_detected: Iterable
    text: Union[AnyStr, Iterable]
    detect_items: Iterable


def pytest_generate_tests(metafunc):
    if BaseUnixDetectTest not in metafunc.cls.mro():
        return

    if metafunc.function.__name__ != 'test_case':
        return metafunc

    idlist = [
        f'Test case {i+1}'
        for i in range(len(metafunc.cls.case_list))
    ]

    argnames = ['is_detected', 'data', 'detect_items']
    argvalues = []

    for is_detected, text, detect_items in metafunc.cls.case_list:
        if isinstance(text, str):
            text = (dedent(text),)
        elif isinstance(text[0], str):
            text = tuple(map(dedent, text))

        argvalues.append((is_detected, text, detect_items))

    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


class BaseUnixDetectTest(ABC):
    @property
    @abstractmethod
    def case_list(self):
        pass

    @property
    @abstractmethod
    def origin_module(self):
        pass

    @property
    @abstractmethod
    def origin_class(self) -> type:
        pass

    def test_case(self, monkeypatch, is_detected, data, detect_items, get_transport_patch):
        monkeypatch.setattr(
            self.origin_module,
            'get_transport',
            partial(get_transport_patch, data=data)
        )
        types._detected = set(is_detected)

        detector = self.origin_class()
        detector.run()
        assert set(detect_items + is_detected) == types._detected
