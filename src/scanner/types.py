import abc
import logging
from enum import Enum
from typing import Union, List, Iterable, AnyStr

from utility import AddLoggerMeta

logger = logging.getLogger(__name__)

_detected = set()


class ControlStatus(Enum):
    NotChecked = 0
    Compliance = 1
    NotCompliance = 2
    NotApplicable = 3
    Error = 4


class TransportMeta(AddLoggerMeta, abc.ABCMeta):
    pass


class BaseControlMeta(abc.ABCMeta, AddLoggerMeta):
    def __str__(self):
        return f'{self.__module__}.{self.__name__}({self.control})'


class BaseDetectorMeta(abc.ABCMeta, AddLoggerMeta):
    pass


def detect_item(name: str) -> None:
    logger.info(f'Item {name} has been detected')
    _detected.add(name)


def is_item_detected(item: str) -> bool:
    result = item in _detected
    logger.debug(f'Is_item_detected: {item} is {result}')
    return result


def reset_detect() -> None:
    _detected.clear()


class BaseTransport(metaclass=TransportMeta):
    @abc.abstractmethod
    def connect(self) -> None:
        pass

    @property
    @abc.abstractmethod
    def is_connect(self) -> bool:
        pass

    @abc.abstractmethod
    def disconnect(self) -> None:
        pass


class BaseDetector(metaclass=BaseDetectorMeta):
    @property
    @abc.abstractmethod
    def requisites(self) -> Union[List[str], str]:
        pass

    @property
    @abc.abstractmethod
    def detection_items(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def detectors(self) -> List:
        pass

    @property
    def requirements(self) -> bool:
        if not self.requisites:
            return True

        if isinstance(self.requisites, str):
            return is_item_detected(self.requisites)

        if isinstance(self.requisites, Iterable):
            return all(map(is_item_detected, self.requisites))

        raise ValueError('Detector.requirements must be str or iterable')

    @abc.abstractmethod
    def detect(self) -> List:
        pass

    def run(self) -> List:
        if not self.requirements:
            return []

        try:
            if not self.detect():
                return []
        except Exception as e:
            self.logger.error(e)
            return []

        detect_item(self.detection_items)
        return self.detectors

    def __repr__(self):
        return f'{self.__class__.__qualname__}()'


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
            if self.control.status == ControlStatus.NotChecked:
                self.control.error(f'{e}')
