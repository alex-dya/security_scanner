import pkg_resources
import logging


control_list = []

LOGGER = logging.getLogger(__name__)


def import_all_controls():
    LOGGER.debug('Start looking for controls')
    for entry_point in pkg_resources.iter_entry_points('.'):
        LOGGER.debug(f'Found control {entry_point.name}')
        entry_point.load()
