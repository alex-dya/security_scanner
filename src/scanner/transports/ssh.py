import paramiko
import socket
import io
import re
import uuid
import time
from typing import NamedTuple, AnyStr, List, Dict, Any

from scanner.types import BaseTransport
from .exceptions import (
    TransportException, AuthenticationFailure, HostNotResponsible)


class Answer(NamedTuple):
    prompt: str
    answer: str


class ExecResult(NamedTuple):
    Output: AnyStr
    Error: AnyStr
    ExitStatus: int


class SSHTransport(BaseTransport):
    errors = [
        'No such file or directory',
        'command not found'
    ]

    class StandartChannels(NamedTuple):
        stdin: io.RawIOBase
        stdout: io.RawIOBase
        stderr: io.RawIOBase

    def __init__(self, config: Dict[str, Any], *args, timeout=30, **kwargs):
        super().__init__(*args, **kwargs)
        ssh_config = config.get('ssh', dict())
        self._login = ssh_config.get('username', '')
        self._password = ssh_config.get('password', '')
        self._address = config['hostname']
        self._port = int(ssh_config.get('port', '22'))
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
            channel.set_combine_stderr(False)
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
            self.logger.debug(f'Host {self._address} is not available')
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

    def disconnect(self) -> None:
        if self._client:
            self._client.close()

    @property
    def is_connect(self):
        transport = self._client.get_transport() if self._client else None
        return transport and transport.is_active()

    def interactive_command(self, command: str, answers_list: List[Answer]=None):
        if answers_list is None:
            answers_list = []

        command = command.strip('\n')
        self.logger.info(f'Send command: {command}')
        finish = f'{uuid.uuid4()}'
        echo_cmd = 'echo {} $?'.format(finish)
        full_command = f'{command}; {echo_cmd}'
        self._shell.stdin.write(f'{full_command} \n')
        self.logger.debug(f'STDIN: {full_command}')
        self._shell.stdin.flush()

        for answer in answers_list:
            time.sleep(0.1)
            self._shell.stdin.write(answer.answer + '\n')
            self.logger.debug(f'STDIN: {answer.answer}')
            self._shell.stdin.flush()

        shell_out = []
        shell_error = []
        line_process = lambda line: re.sub(r'.\r', '', str(line).strip())
        exit_status = 0
        for line in map(line_process, self._shell.stdout):
            if any(e in line for e in self.errors):
                self.logger.debug(f'STDERR: {line!r}')
                shell_error.append(line)
                continue

            self.logger.debug(f'STDOUT: {line!r}')
            if full_command in line:
                # up for now filled with shell junk from stdin
                shell_out = []
                continue

            if line.startswith(finish):
                # our finish command ends with the exit status
                exit_status = int(line.rsplit(maxsplit=1)[1])
                break
            else:
                # get rid of 'coloring and formatting' special characters
                line = re.compile(r'(\x9B|\x1B\[)[0-9]*[ -/]*').\
                    sub('', line).replace('\b', '').replace('\r', '').strip()

                shell_out.append(line)

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
        self.logger.debug('Out: {}'.format(shell_out))
        return ExecResult(
            Output=join_str(shell_out),
            Error=join_str(shell_error),
            ExitStatus=exit_status)
