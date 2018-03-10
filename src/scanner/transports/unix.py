from enum import Enum
from typing import List

from .ssh import SSHTransport, Answer, ExecResult
from scanner.mappings import unameOS


class RootLogonType(Enum):
    NoLogon = 0
    SULogon = 1
    SudoLogon = 2


class UnixTransport(SSHTransport):
    def __init__(self, *args,  root_password,
                 root_logon=RootLogonType.NoLogon, **kwargs):
        super().__init__(*args, **kwargs)
        self._root_logon = root_logon
        self._root_password = root_password

    def _su_logon(self):
        result = self.interactive_command('su - root', answers_list=[
            Answer('Password:', self._root_password)
        ])

    def _sudo_logon(self):
        result = self.interactive_command('su - root', answers_list=[
            Answer(f'[sudo] password for {self._login}:', self._root_password)
        ])

    def is_unix(self):
        result = self.send_command('uname -o')
        if result.Output:
            try:
                os = unameOS(result.Output)
                return True
            except KeyError as e:
                self.logger.error(f'Uname error {e}')
                pass
        return False

    def interactive_command(self, command: str,
                            answers_list: List[Answer]=[]) -> ExecResult:
        command = f'LANG=C LC_CTYPE=C {command}'
        return super().interactive_command(command, answers_list)

    def send_command(self, command: str) -> ExecResult:
        return self.interactive_command(command)
