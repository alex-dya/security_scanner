from textwrap import dedent
from scanner.functions.unix.systemd import SystemdUnitParser


def test_simple_case():
    data = '''
    [Unit]
    Description=Rescue Shell
    Documentation=man:sulogin(8)

    [Service]
    WorkingDirectory=-/root
    ExecStart=-/lib/systemd/systemd-sulogin-shell rescue
    '''
    parser = SystemdUnitParser(dedent(data.strip()))
    result = parser.get_dict()
    assert result == dict(
        Unit=dict(
            Description=['Rescue Shell'],
            Documentation=['man:sulogin(8)']
        ),
        Service=dict(
            WorkingDirectory=['-/root'],
            ExecStart=['-/lib/systemd/systemd-sulogin-shell rescue']
        )
    )


def test_duplcated_options():
    data = '''
    [Unit]
    Description=Emergency Shell
    Documentation=man:sulogin(8)
    Conflicts=shutdown.target
    Conflicts=rescue.service
    Before=shutdown.target
    Before=rescue.service

    [Service]
    WorkingDirectory=-/root
    ExecStart=-/lib/systemd/systemd-sulogin-shell emergency
    '''
    parser = SystemdUnitParser(dedent(data.strip()))
    result = parser.get_dict()
    assert result == dict(
        Unit=dict(
            Description=['Emergency Shell'],
            Documentation=['man:sulogin(8)'],
            Conflicts=['shutdown.target', 'rescue.service'],
            Before=['shutdown.target', 'rescue.service']
        ),
        Service=dict(
            WorkingDirectory=['-/root'],
            ExecStart=['-/lib/systemd/systemd-sulogin-shell emergency']
        )
    )


def test_wrong_unit_files():
    data = '''

    fasdfsadf
    fdaf
    '''
    parser = SystemdUnitParser(dedent(data.strip()))
    result = parser.get_dict()
    assert result == dict()
