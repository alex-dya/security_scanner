import logging
from collections import deque

from .is_unix import UnixDetector


_detectors = [
    UnixDetector()
]

LOGGER = logging.getLogger(__name__)


def detect():
    queue = deque(_detectors)
    while queue:
        detector = queue.popleft()
        LOGGER.debug(f'Run detector {detector!r}')

        result = detector.run()
        LOGGER.debug(f'Result: {result}')

        for new_detector in result:
            queue.append(new_detector)
