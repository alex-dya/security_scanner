class TransportException(Exception):
    def __init__(self, address, port):
        self.address = address
        self.port = port


class HostNotResponsible(TransportException):
    pass


class AuthenticationFailure(TransportException):
    def __init__(self, login, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = login
        self.password = password


class CommandExecutionFailure(TransportException):
    def __init__(self, command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command


class RootLogonFailure(CommandExecutionFailure):
    pass


class WrongInteractiveAnswer(CommandExecutionFailure):
    def __init__(self, answer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answer = answer


class TransportIsDisabled(Exception):
    pass
