import abc
from enum import Enum
from traceback import format_exc
from typing import AnyStr

from scanner.transports import get_transport
from utility import AddLoggerMeta


class ControlStatus(Enum):
    NotChecked = 0
    Compliance = 1
    NotCompliance = 2
    NotApplicable = 3
    Error = 4


class BaseControlMeta(abc.ABCMeta, AddLoggerMeta):
    def __str__(self):
        return f'{self.__module__}.{self.__name__}({self.control})'


class ControlResult:
    controls = {}

    def __new__(cls, number: int, *args, **kwargs) -> 'ControlResult':
        if number in cls.controls:
            return cls.controls[number]

        control = super(ControlResult, cls).__new__(cls, *args, **kwargs)
        cls.controls[number] = control
        return control

    def __init__(self, number: int):
        self.number = number
        self.result = None
        self.status = ControlStatus.NotChecked

    def not_applicable(self) -> None:
        self.status = ControlStatus.NotApplicable
        self.result = None

    def compliance(self, result: str) -> None:
        self.status = ControlStatus.Compliance
        self.result = result

    def not_compliance(self, result: str) -> None:
        self.status = ControlStatus.NotCompliance
        self.result = result

    def error(self, result: str) -> None:
        self.status = ControlStatus.Error
        self.result = result

    def __repr__(self) -> AnyStr:
        return f'ControlResult(number={self.number})'

    def __str__(self) -> AnyStr:
        return f'number={self.number} status={self.status}'


class BaseContol(metaclass=BaseControlMeta):
    _control_list = []
    get_transport = staticmethod(get_transport)

    def __init_subclass__(cls, control_number):
        super().__init_subclass__()
        cls.control = ControlResult(number=control_number)
        cls._control_list.append(cls())

    def __init__(self):
        self.control.status = ControlStatus.NotChecked

    @abc.abstractmethod
    def prerequisite(self) -> bool:
        pass

    @abc.abstractmethod
    def check(self) -> None:
        pass

    @property
    def result(self) -> AnyStr:
        return self.control.result

    def __str__(self) -> AnyStr:
        return f'{self.__class__.__module__}.{self.__class__.__name__}' \
               f'({self.control})'

    def run(self) -> None:
        if not self.prerequisite():
            return

        try:
            self.check()
        except Exception as e:
            self.logger.error(f'{e}')
            self.logger.error(format_exc())
            if self.control.status == ControlStatus.NotChecked:
                self.control.error(f'{e}')
