"""Utilities for exporting data into XML files."""

import xml.etree.ElementTree as ET

def _xml_element(tree: ET.ElementTree, data: any, tagname: str) -> None:
    """Construct an XML element around data and insert it into a XML tree.

    :param tree: The element tree to place the element into.
    :type tree: ET.ElementTree
    :param data: Data to wrap with a XML element.
    :type data: any
    :param tagname: The desired name of the element.
    :type tagname: str
    """

    tree.start(tagname, {})
    tree.data(str(data))
    tree.end(tagname)

def _xml_list(root_el_name: str, child_el_name: str, items: list[any]) -> ET.ElementTree:
    """Express a list of items as XML.

    :param root_el_name: The name of the root XML element.
    :type root_el_name: str
    :param child_el_name: The name of each child elements.
    :type child_el_name: str
    :param items: The name of the root XML element.
    :type items: list
    :return: The XML structure representing the list of `items`.
    :type root_el_name: ET.ElementTree
    """

    tree = ET.TreeBuilder()
    tree.start(root_el_name, {})
    for item in items:
        _xml_element(tree, item, tagname=child_el_name)
    tree.end(root_el_name)
    element = tree.close()
    return _pretty_xml(element)

def _pretty_xml(element: ET.Element) -> ET.ElementTree:
    """Return a prettified (indented) XML.

    :param element: An XML element, usually a root element.
    :type element: ET.Element
    :return: A prettified version of `element`. If `element` is already prettified it will be
    unchanged.
    :rtype: ET.ElementTree
    """

    xml = ET.ElementTree(element)
    ET.indent(xml)
    return xml

def export(root_el_name: str, child_el_name: str, items: list[any], path: str) -> None:
    """Export a list of items into a XML file. If the file at `path` already exists, it will be
    overwritten!

    :param root_el_name: The name of the root XML element.
    :type root_el_name: str
    :param child_el_name: The name of each of the child element.
    :type child_el_name: str
    :param items: The list of items.
    :type items: list
    :param path: The path to the file to write the XML to.
    :type path: str
    """

    _xml_list(root_el_name, child_el_name, items).write(path, encoding='utf-8')
