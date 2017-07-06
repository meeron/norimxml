"""Module implementing Xml document"""

import re


class XmlError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class XmlElement:
    """Xml element class"""

    def __init__(self, name):
        validate_element_name(name)
        self.children = []
        self.name = name
        self._text = None

    def set_text(self, text):
        self._text = encode_text(text)

    def add_child(self, name, text=None):
        if not isinstance(name, str):
            raise TypeError("Only string can be element name.")
        element = XmlElement(name)
        element.set_text(text)
        self.children.append(element)

    def add_element(self, element):
        if element is None:
            raise AttributeError("'element' could not be None.")
        if not isinstance(element, XmlElement):
            raise TypeError("'%s' argument is not XmlElement type")
        self.children.append(element)

    def get_str(self):
        if self._text is None and len(self.children) == 0:
            return "<{}/>".format(self.name)

        element_text = "<{}>".format(self.name)
        if self._text is not None:
            element_text += self._text

        for child in self.children:
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
    if text is None:
        return None

    # TOOD: Do encoding more elegant
    text = re.sub(r'&', r'&amp;', text)
    text = re.sub(r'<', r'&lt;', text)
    text = re.sub(r'>', r'&gt;', text)
    text = re.sub(r"'", r'&apos;', text)
    text = re.sub(r'"', r'&quot;', text)
    return text
