import pytest

from scanner.functions.parsers import KeyValueParser


def test_simple_case():
    text = '''
    NAME=UBUNTU
    ID=ubuntu
    ID_LIKE=debian
    '''

    result = KeyValueParser(text=text)
    assert result is not None
    assert result.NAME == 'UBUNTU'
    assert result.ID == 'ubuntu'
    assert result.ID_LIKE == 'debian'
    assert result.result['NAME'] == 'UBUNTU'
    assert result.result['ID'] == 'ubuntu'
    assert result.result['ID_LIKE'] == 'debian'


def test_double_quotes():
    text = '''
    NAME="UBUNTU"
    ID="ubuntu"
    ID_LIKE=debian
    '''

    result = KeyValueParser(text=text)
    assert result is not None
    assert result.NAME == 'UBUNTU'
    assert result.ID == 'ubuntu'
    assert result.ID_LIKE == 'debian'
    assert result.result['NAME'] == 'UBUNTU'
    assert result.result['ID'] == 'ubuntu'
    assert result.result['ID_LIKE'] == 'debian'


def test_wrong_key():
    text = '''
    NAME="UBUNTU"
    ID="ubuntu"
    ID_LIKE=debian
    '''

    result = KeyValueParser(text=text)
    assert result is not None
    with pytest.raises(AttributeError):
        result.WRONG_KEY


def test_another_delimiter():
    text = '''
    NAME: "UBUNTU"
    ID: "ubuntu"
    ID_LIKE: debian:
    '''

    result = KeyValueParser(text=text, delimiter=':')
    assert result is not None
    assert result.NAME == 'UBUNTU'
    assert result.ID == 'ubuntu'
    assert result.ID_LIKE == 'debian:'
