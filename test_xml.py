"""Testing module"""

import xml.etree.ElementTree as ET
import pytest
from norimxml import XmlDoc, XmlError, XmlElement


class TestXml:
    """Test class"""

    def test_simple_xml(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)
        xml_doc.set_text("Test string")
        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name
        print(xml_doc.get_str())

    def test_encode_string(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)
        xml_doc.set_text('<This "text" should< be \'encoded\' & this>')
        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name

    def test_proper_item_name(self):
        invalid_names = [
            "Items Items",
            "123Items",
            "xmlItems",
            "XMLItems",
            "XmlItems",
            "Item<",
            "Item>",
            "Item&",
            "Item'",
            "Item\""
        ]
        for name in invalid_names:
            with pytest.raises(XmlError) as err:
                xml_doc = XmlDoc(name)
                ET.fromstring(xml_doc.get_str())

    def test_xml_with_children(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)

        xml_doc.add_child("Item1", "Item text")
        xml_doc.add_child("Item2")

        xml_doc.add_element(XmlElement("Item3"))

        element4 = XmlElement("Item4")
        element4.set_text("Item 4 text")
        xml_doc.add_element(element4)

        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name

    def test_xml_nested_elements(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)

        element = XmlElement("Item")
        element.add_child("id", "1")
        element.add_child("name", "Element 1 name")

        props = XmlElement("props")
        props.add_child("prop1", "prop1 value")
        props.add_child("prop2", "prop2 value")
        element.add_element(props)

        xml_doc.add_element(element)

        element = XmlElement("Item")
        element.add_child("id", "2")
        element.add_child("name", "Element 2 name")
        xml_doc.add_element(element)

        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name

    def test_attributes(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)

        element = XmlElement("Item")
        element.add_attribute("id", "element 1")
        element.add_attribute("name", "element name")
        xml_doc.add_element(element)

        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name

    def test_attribute_invalid_name(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)

        element = XmlElement("Item")
        with pytest.raises(XmlError) as err1:
            element.add_attribute("id<", "element 1")
        with pytest.raises(XmlError) as err2:
            element.add_attribute("id>", "element 1")
        with pytest.raises(XmlError) as err3:
            element.add_attribute("id&", "element 1")
        with pytest.raises(XmlError) as err4:
            element.add_attribute("id'", "element 1")
        with pytest.raises(XmlError) as err5:
            element.add_attribute("id\"", "element 1")
        xml_doc.add_element(element)

        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name

    def test_encoding_attribute_value(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)

        element = XmlElement("Item")
        element.add_attribute("id", "<value> & 'test' and \"test\"")
        xml_doc.add_element(element)

        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name
