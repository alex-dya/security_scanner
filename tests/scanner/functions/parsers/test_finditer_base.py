import re

from scanner.functions.parsers import FinditerBase


class IDParser(FinditerBase):
    pattern = r'^\s*ID:\s*(?P<ID>\S+)\s*$'

    flags = re.MULTILINE


def test_simple_case():
    text = '''
    ID: 115
    ID: 120
    '''

    expected_results = '115', '120'
    result = IDParser(text=text)
    assert len(list(iter(result))) == 2
    for number, item in enumerate(result):
        assert item.ID == expected_results[number]


def test_empty_case():
    text = ''
    result = IDParser(text=text)
    assert len(list(iter(result))) == 0

