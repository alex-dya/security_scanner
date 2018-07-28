from scanner.types import ControlStatus
from scanner.controls.unix.linux.filesystem import mounting_is_disabled
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestMountingIsDisabled(BaseUnixControlTest):
    origin = mounting_is_disabled
    case_list = [
        (
            (
                ''' 
                Module                  Size  Used by
                fuse                   98304  1
                ''',
                'install /bin/true',
                'install /bin/true',
                'install /bin/true',
                'install /bin/true',
                'install /bin/true',
                'install /bin/true',
                'install /bin/true',
                'install /bin/true',

            ),
            ControlStatus.Compliance,
            '''
            cramfs is disabled
            freevxfs is disabled
            jffs2 is disabled
            hfs is disabled
            hfsplus is disabled
            squashfs is disabled
            udf is disabled
            vfat is disabled
            '''
        ),
        (
            (
                ''' 
                Module                  Size  Used by
                fuse                   98304  1
                btrfs                1060864  0
                xor                    24576  1 btrfs
                raid6_pq              110592  1 btrfs
                ''',
                '',
                'insmod /lib/modules/4.9.0-6-amd64/kernel/fs/freevxfs/freevxfs.ko',
                '',
                '',
                '',
                '',
                '',
                '',

            ),
            ControlStatus.NotCompliance,
            '''
            cramfs is not disabled
            freevxfs is not disabled
            jffs2 is not disabled
            hfs is not disabled
            hfsplus is not disabled
            squashfs is not disabled
            udf is not disabled
            vfat is not disabled
            '''
        ),
    ]
