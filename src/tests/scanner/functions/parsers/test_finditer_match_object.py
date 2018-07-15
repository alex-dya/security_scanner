import re

import pytest

from scanner.functions.parsers import FinditerMatchObject


def test_simple_case():
    match_object = re.match(pattern='ID:\s*(?P<ID>.*)', string='ID: 115')
    result = FinditerMatchObject(match_object)
    assert result is not None
    assert result.ID == '115'


def test_immutable_object():
    match_object = re.match(pattern='ID:\s*(?P<ID>.*)', string='ID: 115')
    result = FinditerMatchObject(match_object)
    with pytest.raises(RuntimeError):
        result.ID = 15

