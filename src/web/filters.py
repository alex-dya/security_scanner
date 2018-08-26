from datetime import timedelta
from math import ceil

from web import app


@app.template_filter()
def timedelta_format(delta: timedelta) -> str:
    if not isinstance(delta, timedelta):
        app.logger.error(type(delta))
        raise ValueError(
            'timedelta_format takes only datetime.timedelta object')

    return str(timedelta(seconds=ceil(delta.total_seconds())))
