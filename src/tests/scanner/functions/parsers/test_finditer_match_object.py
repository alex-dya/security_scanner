import re

from scanner.functions.parsers import FinditerMatchObject


def test_simple_case():
    match_object = re.match(pattern='ID:\s*(?P<ID>.*)', string='ID: 115')
    result = FinditerMatchObject(match_object)
    assert result is not None
    assert result.ID == '115'
