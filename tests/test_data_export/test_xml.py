"""Test the data_export/xml.py module."""

import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from data_export.xml import export

class TestXMLDataExport(unittest.TestCase):
    """Test the functioning of the data_export/xml.py module."""

    # @patch('data_export.xml._xml_list')
    @patch('data_export.xml.ET.ElementTree.write')
    def test_export(self, write_element_tree: ET.ElementTree) -> None:
        """Confirm that a list of items is exported into a .xml file."""

        items = ['Item 1', 'Item 2', 'Item 3']
        export(root_el_name='Items', child_el_name='Item', items=items, path='/path/to/a/file.xml')
        args, kwargs = write_element_tree.call_args
        self.assertEqual(('/path/to/a/file.xml',), args)
        self.assertEqual({'encoding': 'utf-8'}, kwargs)
