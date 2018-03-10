from enum import Enum
from typing import List

from .ssh import SSHTransport, Answer


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

    def interactive_command(self, command: str, answers_list: List[Answer]=None):
        command = f'LANG=C LC_CTYPE=C {command}'
        return super().interactive_command(command, answers_list)

    def send_command(self, command: str):
        return self.interactive_command(command)
