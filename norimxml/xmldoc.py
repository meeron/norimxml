"""Module implementing Xml document"""

import re


class XmlError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class XmlElement:
    """Xml element class"""

    def __init__(self, name):
        validate_element_name(name)
        self.childs = []
        self.name = name
        self._text = ""

    def set_text(self, text):
        self._text = encode_text(text)

    def get_str(self):
        element_text = "<{}>".format(self.name)
        element_text += self._text

        for child in self.childs:
            element_text += child.get_str()

        element_text += "</{}>".format(self.name)

        return element_text


class XmlDoc(XmlElement):
    """Xml document class"""

    _DECLARATION = '<?xml version="1.0"?>'

    def __init__(self, root_name):
        super().__init__(root_name)

    def get_str(self):
        return XmlDoc._DECLARATION + super().get_str()


def validate_element_name(name):
    pattern = r'^([0-9]|xml|XML|Xml)|\s'
    match = re.search(pattern, name)
    if match:
        raise XmlError("Invalid element name: %s" % name)

def encode_text(text):
    # TOOD: Do encoding more elegant
    text = re.sub(r'&', r'&amp;', text)
    text = re.sub(r'<', r'&lt;', text)
    text = re.sub(r'>', r'&gt;', text)
    text = re.sub(r"'", r'&apos;', text)
    text = re.sub(r'"', r'&quot;', text)
    return text
