from scanner.functions.unix.lsmod_parser import LsmodParser


def test_simple_case():
    text = 'usbcore               253952  5 usbhid,ehci_hcd,ohci_pci,ohci_hcd,ehci_pci'
    result = list(LsmodParser(text=text))
    assert len(result) == 1
    item = result[0]
    assert item.Name == 'usbcore'
    assert item.Size == 253952
    assert item.Number == 5
    assert item.Modules == (
        'usbhid', 'ehci_hcd', 'ohci_pci', 'ohci_hcd', 'ehci_pci')


def test_without_modules():
    text = 'i2c_piix4              24576  0'
    result = list(LsmodParser(text=text))
    assert len(result) == 1
    item = result[0]
    assert item.Name == 'i2c_piix4'
    assert item.Size == 24576
    assert item.Number == 0
    assert item.Modules == tuple()


def test_multiple_lines():
    text = '''
    Module                  Size  Used by
    fuse                   98304  1
    btrfs                1060864  0
    xor                    24576  1 btrfs
    raid6_pq              110592  1 btrfs
    '''
    expected_list = (
        ('fuse', 98304, 1, tuple()),
        ('btrfs', 1060864, 0, tuple()),
        ('xor', 24576, 1, ('btrfs',)),
        ('raid6_pq', 110592, 1, ('btrfs',))
    )
    actual_list = list(LsmodParser(text=text))
    assert len(actual_list) == len(expected_list)
    for actual, expected in zip(actual_list, expected_list):
        assert actual.Name == expected[0]
        assert actual.Size == expected[1]
        assert actual.Number == expected[2]
        assert actual.Modules == expected[3]

