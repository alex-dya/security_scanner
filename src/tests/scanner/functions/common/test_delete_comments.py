from scanner.functions.common import delete_comments


def test_simple_case():
    text = '''
    # some comments
    text
    '''
    assert delete_comments(text) == 'text'


def test_other_prefix():
    text = '''
    // some comments
    / text
    another text
    '''
    assert delete_comments(text, prefix='//') == '/ text\nanother text'


def test_multiple_prefixes():
    text = '''
    // some comments
    # yeat another comments
    / text
    another text
    '''
    assert delete_comments(text, prefix=('//', '#')) == '/ text\nanother text'


def test_empty_text():
    assert delete_comments('') == ''
