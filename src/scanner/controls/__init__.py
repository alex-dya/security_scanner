import importlib
from pathlib import Path
import logging

LOGGER = logging.getLogger(__name__)


def import_all_controls():
    LOGGER.debug('Start looking for controls')
    for module in Path('scanner/controls').glob('**/*.py'):
        if str(module.name) == '__init__.py':
            continue

        LOGGER.debug(f'Found control {module}')
        path = str(module.parent.joinpath(module.stem)).replace('/', '.')
        LOGGER.debug(f'Import path {path}')
        importlib.import_module(path)

import_all_controls()
