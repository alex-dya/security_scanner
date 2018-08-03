import importlib
from pathlib import Path
from os import sep
import logging
from operator import attrgetter

from scanner.types import BaseContol


LOGGER = logging.getLogger(__name__)


def import_all_controls():
    main_path = Path(__file__).parent

    for module in main_path.glob('**/*.py'):
        if module.match('**/__init__.py'):
            continue

        path = str(module.relative_to(main_path).parent.joinpath(module.stem))
        path = '.'.join((__name__, path.replace(sep, '.')))
        importlib.import_module(path.replace(sep, '.'))


def run_controls():
    for control in BaseContol._control_list:
        LOGGER.debug(f'Execute control: {control}')
        control.run()


def result():
    for control in sorted(BaseContol._control_list,
                          key=attrgetter('control.number')):
        yield control


import_all_controls()
