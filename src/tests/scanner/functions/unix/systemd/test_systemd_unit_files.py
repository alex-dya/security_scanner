from textwrap import dedent
from scanner.functions.unix.systemd import SystemdUnitFiles


def test_simple_case():
    data = '''
    home.mount                                                  generated
    '''
    result = list(SystemdUnitFiles(dedent(data.strip())))
    assert len(result) == 1
    item = result[0]
    assert item.UnitName == 'home.mount'
    assert item.Name == 'home'
    assert item.Type == 'mount'
    assert item.State == 'generated'


def test_complex_name():
    data = 'dbus-org.freedesktop.ModemManager1.service                enabled '
    result = list(SystemdUnitFiles(dedent(data.strip())))
    assert len(result) == 1
    item = result[0]
    assert item.UnitName == 'dbus-org.freedesktop.ModemManager1.service'
    assert item.Name == 'dbus-org.freedesktop.ModemManager1'
    assert item.Type == 'service'
    assert item.State == 'enabled'
