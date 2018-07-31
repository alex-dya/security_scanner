import logging
from scanner import transports, types, controls
from scanner.detect import detect


logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


def scan(config: dict) -> list:
    transports.config = config
    detect()
    controls.run_controls()
    return controls.result()


def main():
    transports.config = dict(
        unix=dict(
            login='vmuser',
            password='P@ssw0rd',
            address='192.168.56.10',
            port=22,
            root_logon='SudoLogon',
            root_password='P@ssw0rd'
        )
    )

    # transport = transports.get_transport('unix')
    detect()
    # transport.send_command('poweroff')
    LOGGER.debug(f'Control list: {types.BaseContol._control_list}')
    controls.run_controls()
    for control in controls.result():
        LOGGER.debug(control)
        LOGGER.debug(control.result)

    # is_unix = transport.is_unix()
    # LOGGER.debug(f'Is unix={# is_unix}')
    # shadow = transport.send_command('cat /etc/shadow')
    # LOGGER.debug()
    # ls_result = transport.send_command('ls -al /etc')
    # LOGGER.debug(f'ls result: \n {ls_result.Output}')


if __name__ == '__main__':
    main()
