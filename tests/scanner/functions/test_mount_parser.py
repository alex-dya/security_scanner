from scanner.functions.mount_parser import MountFinditer


def test_simple_case():
    text = 'sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)'
    result = list(MountFinditer(text=text))
    assert len(result) == 1
    item = result[0]
    assert item.Device == 'sysfs'
    assert item.Path == '/sys'
    assert item.Type == 'sysfs'
    assert item.Options == ['rw', 'nosuid', 'nodev', 'noexec', 'relatime']
