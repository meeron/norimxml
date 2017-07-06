"""Module implementing Xml document"""


class XmlElement:
    """Xml element class"""

    def __init__(self, name):
        self.childs = []
        self.name = name

    def get_str(self):
        element_text = "<{}>".format(self.name)

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

