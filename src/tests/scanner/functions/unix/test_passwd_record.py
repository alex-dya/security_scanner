import pytest

from scanner.functions.unix.passwd_parser import PasswdRecord


def test_simple_case():
    line = 'sync:x:4:65534:sync:/bin:/bin/sync'
    result = PasswdRecord(*line.split(':'))
    assert result is not None
    assert result.Name == 'sync'
    assert result.Password == 'x'
    assert result.UID == 4
    assert result.GID == 65534
    assert result.Gecos == 'sync'
    assert result.HomeDirectory == '/bin'
    assert result.Shell == '/bin/sync'


def test_empty_case():
    line = ''
    with pytest.raises(TypeError):
        PasswdRecord(*line.split(':'))
