from . import exceptions
from .ssh import SSHTransport
from .unix import UnixTransport


transports_classes = {
    'ssh': SSHTransport,
    'unix': UnixTransport
}

_transports = dict()


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
