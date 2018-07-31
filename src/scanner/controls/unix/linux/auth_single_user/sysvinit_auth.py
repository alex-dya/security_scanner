from scanner.const.linux import init_subsystem
from scanner.functions.common import delete_comments
from scanner.functions.parsers import KeyValueParser
from scanner.functions.unix.inittab_parser import InittabParser
from scanner.functions.unix.passwd_parser import PasswdParser
from scanner.functions.unix.shadow_parser import ShadowParser
from scanner.transports import get_transport
from scanner.types import BaseContol, is_item_detected


class Control(BaseContol, control_number=8):
    def prerequisite(self):
        return is_item_detected(init_subsystem.SYS_V_INIT)

    @staticmethod
    def _root_has_password(passwd, shadow):
        if not any((passwd, shadow)):
            return False

        if shadow:
            return any(
                user
                for user in ShadowParser(shadow)
                if user.Name == 'root'
                if user.Password
                if user.Password not in ('!', 'x', '!!')
            )

        return any(
            user
            for user in PasswdParser(passwd)
            if user.Name == 'root'
            if user.Password
            if user.Password not in ('!', 'x', '!!')
        )

    @staticmethod
    def _ok_inittab(inittab):
        if not inittab:
            return False

        return any(
            item
            for item in InittabParser(inittab)
            if item.Levels == 'S'
            if item.Action == 'respawn'
            if '/sbin/sulogin' in item.Command
        )

    @staticmethod
    def _ok_sysconfig(sysconfig_init):
        sysconfig_init = delete_comments(sysconfig_init)
        if not sysconfig_init:
            return False

        try:
            return KeyValueParser(sysconfig_init).SINGLE == '/sbin/sulogin'
        except AttributeError:
            return False

    def check(self):
        transport = get_transport('unix')

        passwd = transport.get_file_content('/etc/passwd').Output
        shadow = transport.get_file_content('/etc/shadow').Output
        inittab = transport.get_file_content('/etc/inittab').Output
        sysconfig_init = transport.get_file_content('/etc/sysconfig/init').Output

        errors = []

        if not self._root_has_password(passwd, shadow):
            errors.append(f'User root does not have password')

        if not self._ok_inittab(inittab):
            errors.append(f'Inittab does not have correct line')

        if not self._ok_sysconfig(sysconfig_init):
            errors.append(
                f'/etc/sysconfig/init does not have right attribute SINGLE')

        if not errors:
            self.control.compliance(
                result='Single user mode is protected with password'
            )
            return

        self.control.not_compliance(
            result='\n'.join(errors)
        )
