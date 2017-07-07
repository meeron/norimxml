"""Module implementing Xml document"""

import re
from collections import OrderedDict


class XmlError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class XmlElement:
    """Xml element class"""

    def __init__(self, name):
        validate_name('element', name)
        self.children = []
        self.name = name
        self._text = None
        self._attributes = OrderedDict()

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

    def add_attribute(self, name, value):
        validate_name('attribute', name)
        self._attributes[name] = encode_text(value)

    def get_str(self):
        attributes = []
        for key in self._attributes:
            attributes.append('{}="{}"'.format(key, self._attributes[key]))
        attributes_string = " ".join(attributes)
        if len(self._attributes) > 0:
            attributes_string = " " + attributes_string

        if self._text is None and len(self.children) == 0:
            return "<{}{}/>".format(self.name, attributes_string)

        element_text = "<{}{}>".format(self.name, attributes_string)
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


def validate_name(node_name, name):
    pattern = r'^([0-9]|xml|XML|Xml)|\s|<|>|&|\'|"'
    match = re.search(pattern, name)
    if match:
        raise XmlError("Invalid %s name: '%s'" % (node_name, name))


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
