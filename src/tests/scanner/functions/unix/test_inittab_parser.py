from scanner.functions.unix.inittab_parser import InittabParser


def test_simple_case():
    data = 'rc::sysinit:/etc/rc.sysinit'
    record_list = list(InittabParser(data))
    assert len(record_list) == 1
    item = record_list[0]
    assert item.Id == 'rc'
    assert item.Levels == '0123456'
    assert item.Action == 'sysinit'
    assert item.Command == ['/etc/rc.sysinit']


def test_comments_pass():
    data = '# somecomments'
    record_list = list(InittabParser(data))
    assert len(record_list) == 0


def test_comple_command():
    data = 'c1:2345:respawn:/sbin/agetty -8 38400 vc/1 linux'
    record_list = list(InittabParser(data))
    assert len(record_list) == 1
    item = record_list[0]
    assert item.Id == 'c1'
    assert item.Levels == '2345'
    assert item.Action == 'respawn'
    assert item.Command == ['/sbin/agetty', '-8', '38400', 'vc/1', 'linux']
