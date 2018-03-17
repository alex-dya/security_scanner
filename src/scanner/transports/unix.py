import time
from enum import Enum
from typing import List


from .ssh import SSHTransport, Answer, ExecResult
from scanner.mappings import unameOS
from scanner.transports.exceptions import RootLogonFailure


class RootLogonType(Enum):
    NoLogon = 0
    SULogon = 1
    SudoLogon = 2


class UnixTransport(SSHTransport):
    def __init__(self, *args,  root_password='',
                 root_logon='NoLogon', **kwargs):
        super().__init__(*args, **kwargs)
        self._root_logon_type = RootLogonType[root_logon]
        self._root_password = root_password
        self.envs = dict(
            LANG='C',
            LC_CTYPE='C',
            HISTFILESIZE='0',
            HISTSIZE='0',
            HISTFILE=None
        )

    def connect(self):
        super().connect()
        self.setting_envs()
        if self._root_logon_type == RootLogonType.SULogon:
            self._su_logon()
        elif self._root_logon_type == RootLogonType.SudoLogon:
            self._sudo_logon()

    def setting_envs(self):
        for key, value in self.envs.items():
            if value is None:
                command = f'unset {key}'
            else:
                command = f'export {key}={value}'
            self.send_command(command)

    def _su_logon(self):
        self._root_logon('su - root', answers_list=[
            Answer('Password:', self._root_password)
        ])

    def _sudo_logon(self):
        self._root_logon('sudo -i', answers_list=[
            Answer(f'[sudo] password for {self._login}:', self._password)
        ])

    def _root_logon(self, command: str, answers_list: List[Answer]=[]):
        command = command.strip('\n')
        self._shell.stdin.write(f'{command}\n')
        self.logger.debug(f'STDIN: {command}')
        self._shell.stdin.flush()

        for answer in answers_list:
            time.sleep(2)
            self._shell.stdin.write(answer.answer + '\n')
            self.logger.debug(f'STDIN: {answer.answer}')
            self._shell.stdin.flush()

        time.sleep(2)
        result = self.interactive_command('id -u')

        self.setting_envs()
        if result.Output != '0':
            raise RootLogonFailure(
                address=self._address,
                port=self._port,
                command=command
            )

    def is_unix(self):
        result = self.send_command('uname -s')
        if not result.Output:
            return False

        if unameOS(result.Output) is not None:
            return True

        return False

    def send_command(self, command: str) -> ExecResult:
        return self.interactive_command(command)
