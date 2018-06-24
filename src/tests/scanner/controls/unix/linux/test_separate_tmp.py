from functools import partial

import pytest

from scanner.types import ControlStatus
from scanner.controls.unix.linux.tmp import separate_tmp


test_cases = [
    (
        ''' 
        sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
        proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
        tmpfs on /tmp type tmpfs (rw,nosuid,nodev,noexec,relatime)
        udev on /dev type devtmpfs (rw,nosuid,relatime,size=3995276k,nr_inodes=998819,mode=755)
        devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
        tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=805012k,mode=755)
        ''',
        ControlStatus.Compliance
    ),
    (
        ''' 
        sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
        proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
        udev on /dev type devtmpfs (rw,nosuid,relatime,size=3995276k,nr_inodes=998819,mode=755)
        devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
        tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=805012k,mode=755)
        ''',
        ControlStatus.NotCompliance
    ),
]


@pytest.mark.parametrize('text,result', test_cases)
def test_cases(monkeypatch, text, result, get_transport_patch):
    monkeypatch.setattr(
        separate_tmp, 'get_transport', partial(get_transport_patch, text=text))
    control = separate_tmp.Control()
    monkeypatch.setattr(separate_tmp, 'is_os_detect', lambda x: True)
    control.run()
    assert control.control.status == result


def test_not_applicable(monkeypatch):
    control = separate_tmp.Control()
    monkeypatch.setattr(separate_tmp, 'is_os_detect', lambda x: False)
    control.run()
    assert control.control.status == ControlStatus.NotApplicable
