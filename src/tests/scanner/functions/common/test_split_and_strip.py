from scanner.functions.common import split_and_strip


def test_simple_case():
    text = 'a b c d'
    assert split_and_strip(text) == ('a', 'b', 'c', 'd')


def test_other_delimeter():
    text = 'a,b,c,d'
    assert split_and_strip(text, delimiter=',') == ('a', 'b', 'c', 'd')


def test_skip_empty_value():
    text = 'a  b  d'
    assert split_and_strip(text) == ('a', 'b', 'd')
    text = '1,,2,3'
    assert split_and_strip(text, delimiter=',') == ('1', '2', '3')


def test_empty_case():
    text = ''
    assert split_and_strip(text) is None
