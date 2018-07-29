import pytest

from scanner.functions.unix.passwd_parser import PasswdParser


def test_simple_case():
    line = 'sync:x:4:65534:sync:/bin:/bin/sync'
    result = list(PasswdParser(line))
    assert len(result) == 1
    item = result[0]
    assert item is not None
    assert item.Name == 'sync'
    assert item.Password == 'x'
    assert item.UID == 4
    assert item.GID == 65534
    assert item.Gecos == 'sync'
    assert item.HomeDirectory == '/bin'
    assert item.Shell == '/bin/sync'


def test_empty_case():
    line = ''
    result = list(PasswdParser(line))
    assert len(result) == 0

