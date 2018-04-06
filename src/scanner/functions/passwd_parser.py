class PasswdRecord:
    Name: str
    Password: str
    UID: int
    GID: int
    Gecos: str
    HomeDirectory: str
    Shell: str

    def __init__(self, line):
        super().__init__()
        (
            name, passwd, uid,
            gid, gecos, home_dir,
            shell
        ) = line.split(':')
        self.Name = name
        self.Password = passwd
        self.UID = int(uid)
        self.GID = int(gid)
        self.Gecos = gecos
        self.HomeDirectory = home_dir
        self.Shell = shell

    def __repr__(self):
        return f'PasswdRecord({self.Name}, {self.UID})'


class PasswdParser:
    def __init__(self, content: str):
        self.content = content

    def __iter__(self):
        self._iter = iter(self.content.splitlines())
        return self

    def __next__(self):
        return PasswdRecord(next(self._iter))
