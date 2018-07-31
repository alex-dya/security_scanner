from typing import AnyStr, Iterable, Optional, Union


def split_and_strip(
        text: AnyStr,
        delimiter: AnyStr = None) -> Optional[Iterable[AnyStr]]:

    if not text:
        return

    return tuple(
        filter(
            None,
            (item.strip() for item in text.split(delimiter))
        )
    )


def delete_comments(
        text: AnyStr,
        prefix: Union[AnyStr, Iterable[AnyStr]] = '#'
) -> AnyStr:

    if not text:
        return text

    return '\n'.join(
        line
        for line in map(str.strip, text.splitlines())
        if line
        if not line.startswith(prefix)
    )
