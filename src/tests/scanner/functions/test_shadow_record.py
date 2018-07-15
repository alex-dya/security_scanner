import pytest

from scanner.functions.shadow_parser import ShadowRecord
from datetime import date


def test_simple_case():
    line = 'speech-dispatcher:!:17536:0:99999:7:::'
    result = ShadowRecord(*line.split(':'))
    assert result is not None
    assert result.Name == 'speech-dispatcher'
    assert result.Password == '!'
    assert result.PasswordChange == date(2018, 1, 5)
    assert result.MinPasswordAge == 0
    assert result.MaxPasswordAge == 99999
    assert result.PasswordWarn == 7
    assert result.PasswordExpired == 99999
    assert result.AccountExpired == 99999
    assert result.ReservedField == ''


def test_empty_case():
    line = ''
    with pytest.raises(TypeError):
        ShadowRecord(*line.split(':'))
