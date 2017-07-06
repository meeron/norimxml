"""Testing module"""

import xml.etree.ElementTree as ET
from norimxml import XmlDoc


class TestXml:
    """Test class"""

    def test_simple_xml(self):
        root_name = "Items"
        xml_doc = XmlDoc(root_name)
        root = ET.fromstring(xml_doc.get_str())
        assert root.tag == root_name
