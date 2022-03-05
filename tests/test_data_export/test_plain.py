"""Test the data_export/plain.py module."""

import unittest
from unittest.mock import Mock, patch, mock_open
from data_export.plain import export

class TestPlainTextDataExport(unittest.TestCase):
    """Test the functioning of the data_export/plain.py module."""

    @patch("builtins.open", new_callable=mock_open)
    def test_export(self, open_: Mock) -> None:
        """Confirm that a list of items is exported into a .txt file."""

        items = ['Item 1', 'Item 2', 'Item 3']
        export(items, path='/path/to/a/file.txt')
        args, kwargs = open_.call_args
        file_write_args, _ = open_.return_value.write.call_args
        self.assertEqual(('/path/to/a/file.txt', 'wt'), args)
        self.assertEqual({'encoding': 'utf-8'}, kwargs)
        self.assertEqual(('Item 1\nItem 2\nItem 3',), file_write_args)
