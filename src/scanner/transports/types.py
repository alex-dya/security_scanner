import abc

from utility import AddLoggerMeta


class TransportMeta(AddLoggerMeta, abc.ABCMeta):
    pass


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
