def split_and_strip(text, delimiter=None):
    if not text:
        return

    return tuple(
        filter(
            None,
            (item.strip() for item in text.split(delimiter))
        )
    )
