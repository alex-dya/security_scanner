from scanner.types import ControlStatus
from scanner.controls.unix.linux.partitions import mount_options
from tests.scanner.controls.conftest import BaseUnixTest


class TestMountOptions(BaseUnixTest):
    origin = mount_options
    case_list = [
        (
            ''' 
            sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
            proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
            tmpfs on /tmp type tmpfs (rw,nosuid,nodev,noexec,relatime)
            ''',
            ControlStatus.NotCompliance,
            '''
            /var/tmp has not been mounted on separated partition
            /home has not been mounted on separated partition
            /dev/shm has not been mounted on separated partition
            /tmp has been mounted with options "nodev,nosuid,noexec"
            '''
        ),
        (
            ''' 
            /dev/sda2 on /home type ext4 (rw,relatime,nodev,space_cache,subvolid=262,subvol=/@/home)
            /dev/sda3 on /var/tmp type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            /dev/sda3 on /dev/shm type ext4 (rw,relatime,nodev,nosuid,noexec,space_cache)
            tmpfs on /tmp type tmpfs (rw,nosuid,nodev,noexec,relatime)
            ''',
            ControlStatus.Compliance,
            '''
            /var/tmp has been mounted with options "nodev,nosuid,noexec"
            /home has been mounted with options "nodev"
            /dev/shm has been mounted with options "nodev,nosuid,noexec"
            /tmp has been mounted with options "nodev,nosuid,noexec"
            '''
        ),
        (
            ''' 
            /dev/sda2 on /home type ext4 (rw,relatime,space_cache,subvolid=262,subvol=/@/home)
            /dev/sda3 on /var/tmp type ext4 (rw,relatime,space_cache)
            /dev/sda3 on /dev/shm type ext4 (rw,relatime,space_cache)
            ''',
            ControlStatus.NotCompliance,
            '''
            /var/tmp has been mounted without options "nodev,nosuid,noexec"
            /home has been mounted without options "nodev"
            /dev/shm has been mounted without options "nodev,nosuid,noexec"
            /tmp has not been mounted on separated partition
            '''
        ),
    ]
