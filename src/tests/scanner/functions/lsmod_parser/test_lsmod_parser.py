from scanner.functions.lsmod_parser import LsmodParser


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


def test_withou_modules():
    text = 'i2c_piix4              24576  0'
    result = list(LsmodParser(text=text))
    assert len(result) == 1
    item = result[0]
    assert item.Name == 'i2c_piix4'
    assert item.Size == 24576
    assert item.Number == 0
    assert item.Modules == tuple()
