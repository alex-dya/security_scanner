from scanner.types import ControlStatus
from scanner.controls.unix.linux.partitions import separate_partitions
from tests.scanner.controls.conftest import BaseUnixControlTest


class TestSeparatePartitions(BaseUnixControlTest):
    origin = separate_partitions
    case_list = [
        (
           '''
            /dev/sda2 on /home type ext4 (rw,relatime,nodev,space_cache,subvolid=262,subvol=/@/home)
            /dev/sda3 on /var type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            /dev/sda4 on /var/log type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            /dev/sda5 on /var/tmp type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            /dev/sda6 on /var/log/audit type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            tmpfs on /tmp type tmpfs (rw,nosuid,nodev,noexec,relatime)
           ''',
            ControlStatus.Compliance,
            '''
            /home has been mounted on /dev/sda2
            /tmp has been mounted on tmpfs
            /var has been mounted on /dev/sda3
            /var/log has been mounted on /dev/sda4
            /var/log/audit has been mounted on /dev/sda6
            /var/tmp has been mounted on /dev/sda5
            '''
        ),
        (
            '''
            /dev/sda2 on /home type ext4 (rw,relatime,nodev,space_cache,subvolid=262,subvol=/@/home)
            /dev/sda3 on /var type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            /dev/sda5 on /var/tmp type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            /dev/sda6 on /var/log/audit type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            tmpfs on /tmp type tmpfs (rw,nosuid,nodev,noexec,relatime)
            ''',
            ControlStatus.NotCompliance,
            '''
            /home has been mounted on /dev/sda2
            /tmp has been mounted on tmpfs
            /var has been mounted on /dev/sda3
            /var/log/audit has been mounted on /dev/sda6
            /var/tmp has been mounted on /dev/sda5
            /var/log has not been mounted on separate partition
            '''
        ),
        (
            '''
            devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
            tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=805020k,mode=755)
            /dev/sda5 on / type btrfs (rw,relatime,ssd,space_cache,subvolid=257,subvol=/@)
            ''',
            ControlStatus.NotCompliance,
            '''
            /home has not been mounted on separate partition
            /tmp has not been mounted on separate partition
            /var has not been mounted on separate partition
            /var/log has not been mounted on separate partition
            /var/log/audit has not been mounted on separate partition
            /var/tmp has not been mounted on separate partition
            '''
        ),
    ]
