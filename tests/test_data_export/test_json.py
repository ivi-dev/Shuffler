"""Test the data_export/json.py module."""

import unittest
from unittest.mock import Mock, patch, mock_open
from data_export.json import export

class TestJsonDataExport(unittest.TestCase):
    """Test the functioning of the data_export/json.py module."""

    @patch("builtins.open", new_callable=mock_open)
    def test_export(self, open_: Mock) -> None:
        """Confirm that a list of items is exported into a .json file."""

        items = ['Item 1', 'Item 2', 'Item 3']
        export(items, path='/path/to/a/file.json')
        args, kwargs = open_.call_args
        file_write_args, _ = open_.return_value.write.call_args
        self.assertEqual(('/path/to/a/file.json', 'wt'), args)
        self.assertEqual({'encoding': 'utf-8'}, kwargs)
        self.assertEqual(('[\n    "Item 1",\n    "Item 2",\n    "Item 3"\n]',), file_write_args)
