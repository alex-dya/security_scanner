import logging
import abc
from typing import List, Union

from utility import AddLoggerMeta

logger = logging.getLogger(__name__)

_detected = set()


def os_detect(os: str) -> None:
    logger.info(f'OS: {os} has been detected')
    _detected.add(os)


def is_os_detect(os: str) -> bool:
    result = os in _detected
    logger.debug(f'Is_os_detected: {os} is {result}')
    return result


class BaseDetectorMeta(abc.ABCMeta, AddLoggerMeta):
    pass


class BaseDetector(metaclass=BaseDetectorMeta):
    @property
    @abc.abstractmethod
    def requisites(self) -> Union[List[str], str]:
        pass

    @property
    @abc.abstractmethod
    def detection_os(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def detectors(self) -> List:
        pass

    @property
    def requirements(self) -> bool:
        if self.requisites:
            if isinstance(self.requisites, List):
                return all(map(is_os_detect, self.requisites))
            return is_os_detect(self.requisites)
        return True

    @abc.abstractmethod
    def detect(self) -> List:
        pass

    def run(self) -> List:
        if self.requirements and self.detect():
            os_detect(self.detection_os)
            return self.detectors
        return []

    def __repr__(self):
        return f'{self.__class__.__qualname__}()'
