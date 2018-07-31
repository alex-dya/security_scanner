import importlib
from pathlib import Path
from os import sep
import sys
import logging
from scanner.types import BaseContol


LOGGER = logging.getLogger(__name__)


def import_all_controls():
    main_path = Path(sys.argv[0]).parent
    for module in main_path.joinpath(__name__.replace('.', sep)).glob('**/*.py'):
        if module.match('**/__init__.py'):
            continue

        path = str(module.relative_to(main_path).parent.joinpath(module.stem))
        importlib.import_module(path.replace(sep, '.'))


def run_controls():
    for control in BaseContol._control_list:
        LOGGER.debug(f'Execute control: {control}')
        control.run()


def result():
    for control in BaseContol._control_list:
        yield control


import_all_controls()
