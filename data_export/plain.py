"""Utilities for exporting data into plain text files."""

def export(items: list[any], path: str) -> None:
    """Export a list of items into a plain text (.txt) file. Each item of the list will be placed on
    a separate line. If the file at `path` already exists, it will be overwritten!

    :param items: The list of items.
    :type items: list
    :param path: The path to the file to write the text to.
    :type path: str
    """

    with open(path, 'wt', encoding='utf-8') as file:
        file.write('\n'.join(items))
