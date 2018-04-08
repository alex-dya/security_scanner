from typing import AnyStr, Iterator


class PasswdRecord:
    Name: str
    Password: str
    UID: int
    GID: int
    Gecos: str
    HomeDirectory: str
    Shell: str

    def __init__(self, name, passwd, uid, gid, gecos, home_dir, shell):
        super().__init__()

        self.Name = name
        self.Password = passwd
        self.UID = int(uid)
        self.GID = int(gid)
        self.Gecos = gecos
        self.HomeDirectory = home_dir
        self.Shell = shell

    def __repr__(self) -> AnyStr:
        return f'PasswdRecord({self.Name}, {self.UID})'


class PasswdParser:
    def __init__(self, content: str):
        self.content = content

    def __iter__(self) -> Iterator:
        self._iter = iter(self.content.splitlines())
        return self

    def __next__(self) -> PasswdRecord:
        line = next(self._iter)
        while not line.strip():
            line = next(self._iter)
        return PasswdRecord(*line.split(':'))
