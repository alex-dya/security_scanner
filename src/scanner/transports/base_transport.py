import abc

from utility import AddLoggerMeta


class TransportMeta(AddLoggerMeta, abc.ABCMeta):
    pass


class BaseTransport(metaclass=TransportMeta):
    @abc.abstractmethod
    def connect(self):
        pass

    @property
    @abc.abstractmethod
    def is_connect(self):
        pass
