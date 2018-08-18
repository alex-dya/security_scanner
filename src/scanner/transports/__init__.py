from typing import Dict

from scanner.types import BaseTransport
from . import exceptions
from .ssh import SSHTransport
from .unix import UnixTransport


transports_classes = {
    'ssh': SSHTransport,
    'unix': UnixTransport
}

_transports: Dict[str, BaseTransport] = dict()

config = dict()


def get_transport(name):
    if name in _transports:
        return _transports[name]

    transport_class = transports_classes.get(name, None)

    if transport_class is None:
        return

    transport = transport_class(config)
    transport.connect()

    _transports[name] = transport

    return transport


def reset_transports():
    for transport in _transports.values():
        transport.disconnect()

    _transports.clear()

