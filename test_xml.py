"""Testing module"""

import xml.etree.ElementTree as ET
import pytest
from norimxml import XmlDoc, XmlError


class TestXml:
    """Test class"""

    def test_simple_xml(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)
        xml_doc.set_text("Test string")
        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name

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
            "XmlItems"
        ]
        for name in invalid_names:
            with pytest.raises(XmlError) as err:
                xml_doc = XmlDoc(name)
                ET.fromstring(xml_doc.get_str())
