import importlib
from pathlib import Path
import logging
from scanner.types import BaseContol

LOGGER = logging.getLogger(__name__)


def import_all_controls():
    LOGGER.debug('Start looking for controls')
    for module in Path('scanner/controls').glob('**/*.py'):
        if str(module.name) == '__init__.py':
            continue

        path = str(module.parent.joinpath(module.stem)).replace('/', '.')
        LOGGER.debug(f'Import path {path}')
        importlib.import_module(path)


def run_controls():
    for control in BaseContol._control_list:
        LOGGER.debug(f'Execute control: {control}')

        control.run()


def result():
    for control in BaseContol._control_list:
        yield control


import_all_controls()
