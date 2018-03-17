import paramiko
import socket
import io
import re
import uuid
import time
from typing import NamedTuple, AnyStr, List

from scanner.types import BaseTransport
from .exceptions import (
    TransportException, AuthenticationFailure, HostNotResponsible,
    WrongInteractiveAnswer)


class Answer(NamedTuple):
    prompt: str
    answer: str


class ExecResult(NamedTuple):
    Output: AnyStr
    Error: AnyStr


class SSHTransport(BaseTransport):
    class StandartChannels(NamedTuple):
        stdin: io.RawIOBase
        stdout: io.RawIOBase
        stderr: io.RawIOBase

    def __init__(self, login, password, address, *args,
                 port=22, timeout=30, **kwargs):
        super().__init__(*args, **kwargs)
        self._login = login
        self._password = password
        self._address = address
        self._port = port
        self._client = paramiko.SSHClient()
        self._timeout = timeout
        self._shell = None

    def __repr__(self):
        return f'SSHTransport(address={self._address}. port={self._port})'

    def __del__(self):
        self._client.close()

    def connect(self):
        try:
            self._client.set_missing_host_key_policy(
                paramiko.MissingHostKeyPolicy())
            self._client.connect(
                hostname=self._address,
                port=self._port,
                username=self._login,
                password=self._password,
                timeout=self._timeout
            )
            channel = self._client.invoke_shell()
            channel.settimeout(2)
            self._shell = self.StandartChannels(
                stdin=channel.makefile('wb'),
                stdout=channel.makefile('r'),
                stderr=channel.makefile_stderr('r')
            )
            self.interactive_command('echo test')
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
        transport = self._client.get_transport() if self._client else None
        return transport and transport.is_active()

    def interactive_command(self, command: str, answers_list: List[Answer]=[]):
        command = command.strip('\n')
        self.logger.info(f'Send command: {command}')
        finish = f'{uuid.uuid4()}'
        echo_cmd = 'echo {} $?'.format(finish)
        full_command = f'{command}; {echo_cmd}'
        self._shell.stdin.write(f'{full_command} \n')
        self.logger.debug(f'STDIN: {full_command}')
        self._shell.stdin.flush()

        for answer in answers_list:
            time.sleep(0.5)
            self._shell.stdin.write(answer.answer + '\n')
            self.logger.debug(f'STDIN: {answer.answer}')
            self._shell.stdin.flush()

        shell_out = []
        shell_error = []
        line_process = lambda line: re.sub(r'.\r', '', str(line).strip())
        for line in map(line_process, self._shell.stdout):
            self.logger.debug(f'STDOUT: {line!r}')
            if full_command in line:
                # up for now filled with shell junk from stdin
                shell_out = []
                continue

            if line.startswith(finish):
                # our finish command ends with the exit status
                exit_status = int(line.rsplit(maxsplit=1)[1])
                if exit_status:
                    # stderr is combined with stdout.
                    # thus, swap shell_error with shell_out in a case of failure.
                    shell_error = self._shell.stderr.read()
                    self.logger.debug(f'STDERR: {shell_error}')
                    # shell_out = []
                break
            else:
                # get rid of 'coloring and formatting' special characters
                shell_out.append(
                    re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                    replace('\b', '').replace('\r', '').strip())

        # first and last lines of shell_out/shell_error contain a prompt
        if shell_out and echo_cmd in shell_out[-1]:
            shell_out.pop()
        if shell_out and command in shell_out[0]:
            shell_out.pop(0)
        if shell_error and echo_cmd in shell_error[-1]:
            shell_error.pop()
        if shell_error and command in shell_error[0]:
            shell_error.pop(0)

        join_str = '\n'.join

        return ExecResult(
            Output=join_str(shell_out),
            Error=join_str(shell_error))
