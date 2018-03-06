import logging


class AddLoggerMeta(type):
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.logger = logging.getLogger('.'.join((obj.__module__, obj.__qualname__)))
        return obj
