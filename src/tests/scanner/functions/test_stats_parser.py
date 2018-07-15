from datetime import datetime
from textwrap import dedent

import pytest

from scanner.functions.stats_parser import StatsParser
from scanner.const import file_type


def test_simple_case():
    text = 'fifo|6644|user|user|0|1531682463|teemp1'
    stats_list = list(StatsParser(text))
    assert len(stats_list) == 1
    item = stats_list[0]
    assert item.Type == file_type.FIFO
    assert item.Permissions == 0o6644
    assert item.Owner == 'user'
    assert item.GroupOwner == 'user'
    assert item.Size == 0
    assert item.ModifyDateTime == datetime(2018, 7, 15, 22, 21, 3)


def test_case_multiline():
    text = '''
    regular file|644|user|group|72|1520361768|main.py
    directory|755|user|group|176|1529866111|scanner
    '''
    text = dedent(text)
    stats_list = list(StatsParser(text))
    assert len(stats_list) == 2
    item = stats_list[0]
    assert item.Type == file_type.FILE
    assert item.Permissions == 0o644
    assert item.Owner == 'user'
    assert item.GroupOwner == 'group'
    assert item.Size == 72
    assert item.ModifyDateTime == datetime(2018, 3, 6, 21, 42, 48)
    item = stats_list[1]
    assert item.Type == file_type.DIRECTORY
    assert item.Permissions == 0o755
    assert item.Owner == 'user'
    assert item.GroupOwner == 'group'
    assert item.Size == 176
    assert item.ModifyDateTime == datetime(2018, 6, 24, 21, 48, 31)


@pytest.mark.parametrize(
    'text,expected',
    [
        (
            'character special file|660|root|tty|0|1531428784|vcs3',
            (
                file_type.CHARACTER_DEVICE, 0o660,
                'root',
                'tty',
                0,
                datetime(2018, 7, 12, 23, 53, 4),
                'vcs3',
            )
        ),
        (
            'symbolic link|777|root|root|15|1531428780|stderr',
            (

                file_type.SYMLINK,
                0o777,
                'root',
                'root',
                15,
                datetime(2018, 7, 12, 23, 53),
                'stderr'
            )
        ),
        (
            'block special file|660|root|disk|0|1531428783|sda',
            (
                file_type.BLOCK_DEVICE,
                0o660,
                'root',
                'disk',
                0,
                datetime(2018, 7, 12, 23, 53, 3),
                'sda'
            )
        ),
        (
            'socket|777|root|root|0|1531428782|/run/systemd/notify ',
            (
                file_type.SOCKET,
                0o777,
                'root',
                'root',
                0,
                datetime(2018, 7, 12, 23, 53, 2),
                '/run/systemd/notify'
            )
        )
    ]
)
def test_parametrised(text, expected):
    text = dedent(text)
    stats_list = list(StatsParser(text))
    assert len(stats_list) == 1
    actual = stats_list[0]
    assert actual.Type == expected[0]
    assert actual.Permissions == expected[1]
    assert actual.Owner == expected[2]
    assert actual.GroupOwner == expected[3]
    assert actual.Size == expected[4]
    assert actual.ModifyDateTime == expected[5]
