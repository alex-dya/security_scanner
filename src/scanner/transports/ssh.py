import paramiko
import socket
from typing import NamedTuple, AnyStr
from .base_transport import BaseTransport
from .exceptions import (
    TransportException, AuthenticationFailure, HostNotResponsible,
    CommandExecutionFailure)


class SSHTransport(BaseTransport):
    class ExecResult(NamedTuple):
        Output: AnyStr
        Error: AnyStr

    def __init__(self, login, password, address, *args,
                 port=22, timeout=30, **kwargs):
        super().__init__(*args, **kwargs)
        self._login = login
        self._password = password
        self._address = address
        self._port = port
        self._client = paramiko.SSHClient()
        self._timeout = timeout

    def __repr__(self):
        return f'SSHTransport(address={self._address}. port={self._port})'

    def connect(self):
        try:
            self._client.set_missing_host_key_policy(
                paramiko.MissingHostKeyPolicy())
            self._client.connect(
                hostname=self._address,
                username=self._login,
                password=self._password,
                timeout=self._timeout

            )
        except paramiko.AuthenticationException:
            self.logger.debug(f'AuthenticationError {self._login}'
                              f' on {self._address}')
            raise AuthenticationFailure(
                login=self._login,
                password=self._password,
                address=self._address,
                port=self._port
            )
        except socket.timeout:
            self.logger.debug(f'Host {self_address} is not available')
            raise HostNotResponsible(
                address=self._address,
                port=self._port
            )
        except paramiko.SSHException:
            self.logger.debug(f'TransportError')
            raise TransportException(
                address=self._address,
                port=self._port
            )

    @property
    def is_connect(self):
        try:
            self._client.exec_command('echo "test"', timeout=self._timeout)
        except RuntimeError:
            return False
        return True

    def send_command(self, command):
        try:
            stdin, stdout, stderr = self._client.exec_command(
                command, timeout=self._timeout)
            return self.ExecResult(
                Output=stdout.read(),
                Error=stderr.read()
            )
        except:
            self.logger.debug(f'Error on execution command {command}')
            raise CommandExecutionFailure(
                address=self._address,
                port=self._port,
                command=command
            )


