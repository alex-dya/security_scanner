import abc
import logging
from typing import Union, List, Iterable

from utility import AddLoggerMeta

_detected = set()
logger = logging.getLogger(__name__)


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
            self.logger.error(f'Detect exception: {e}')
            return []

        detect_item(self.detection_items)
        return self.detectors

    def __repr__(self):
        return f'{self.__class__.__qualname__}()'
