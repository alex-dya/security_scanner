import pytest

from scanner.functions.unix.shadow_parser import ShadowParser
from datetime import date


def test_simple_case():
    line = 'speech-dispatcher:!:17536:0:99999:7:::'
    result = list(ShadowParser(line))
    assert len(result) == 1
    item = result[0]
    assert item is not None
    assert item.Name == 'speech-dispatcher'
    assert item.Password == '!'
    assert item.PasswordChange == date(2018, 1, 5)
    assert item.MinPasswordAge == 0
    assert item.MaxPasswordAge == 99999
    assert item.PasswordWarn == 7
    assert item.PasswordExpired == 99999
    assert item.AccountExpired == 99999
    assert item.ReservedField == ''


def test_empty_case():
    line = ''
    result = list(ShadowParser(line))
    assert len(result) == 0
