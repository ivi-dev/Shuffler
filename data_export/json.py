"""Utilities for exporting data into JSON files."""

import json

def export(items: list[any], path: str) -> None:
    """Export a list of items into a JSON file. If the file at `path` already exists, it will be
    overwritten!

    :param items: The list of items.
    :type items: list
    :param path: The path to the file to write the JSON string to.
    :type path: str
    """

    json_ = json.dumps(items, indent=4)
    with open(path, 'wt', encoding='utf-8') as file:
        file.write(json_)
