import os
from log_helper import logger
import xml.etree.ElementTree as XmlTree
import xml.dom.minidom as minidom


class BaseDictionaryProvider:
    """
    Base class for all dictionary providers
    """
    def __init__(self, file_path, read_only):
        """
        Common properties for all dictionary providers (read-only, file path, dictionary name)
        :param file_path: Path to dictionary file
        :param read_only: True if dictionary is read-only
        """
        self.file_path = file_path
        if not os.path.isfile(self.file_path):
            raise RuntimeError("File does not exist: %s" % self.file_path)

        logger.info("Parse dictionary %s" % file_path)
        self.dictionary_name = os.path.splitext(os.path.basename(self.file_path))[0]
        self.read_only = read_only

    def name(self):
        """
        :return: Dictionary name
        """
        return self.dictionary_name

    def path(self):
        """
        :return: Path to dictionary file
        """
        return self.file_path


class IdeaDictionaryProvider(BaseDictionaryProvider):
    """
    Provider class for dictionary in IDEA format.
    IDEA dictionary format is XML with pre-defined structure:
    <component name="ProjectDictionaryState">
        <dictionary name="username">
            <words>
                <w>Cortana</w>
                <w>Filesize</w>
            </words>
        </dictionary>
    </component>
    <component name="CachedDictionaryState">
        <dictionary name="username">
            <words>
                <w>Cortana</w>
                <w>Filesize</w>
            </words>
        </dictionary>
    </component>
    DictionaryProvider class has read() and write(new_dictionary) methods
    """

    def __init__(self, file_path, read_only=False):
        """
        Open IDEA XML dictionary file
        :param file_path: Relative or absolute path to file
        :raise: RuntimeError if file does not exist
        """
        super(IdeaDictionaryProvider, self).__init__(file_path, read_only)
        self.idea_dictionary = []
        tree = XmlTree.parse(self.path())
        root = tree.getroot()

        # iterate all components and collect all words from all dictionaries
        for word in root.findall("./dictionary/words/w"):
            self.idea_dictionary.append(word.text)

    def read(self):
        """
        :return: List of dictionary items
        """
        return self.idea_dictionary

    def write(self, new_dictionary):
        """
        :param new_dictionary: New dictionary to write, normally merged from different sources
        """
        if self.read_only:
            logger.warning("Read-only dictionary, skip writing")
            return

        doc = minidom.Document()

        component = doc.createElement("component")
        component.setAttribute("name", "ProjectDictionaryState")
        doc.appendChild(component)

        dictionary = doc.createElement("dictionary")
        dictionary.setAttribute("name", self.dictionary_name)
        component.appendChild(dictionary)

        words = doc.createElement("words")
        dictionary.appendChild(words)

        for item in new_dictionary:
            w = doc.createElement("w")
            dict_item = doc.createTextNode(item)
            w.appendChild(dict_item)
            words.appendChild(w)

        xml_text = doc.toprettyxml(indent="  ")
        with open(self.path(), "w", encoding="utf-8") as idea_dict:
            idea_dict.write(xml_text)


class PlaintextDictionaryProvider(BaseDictionaryProvider):
    """
    Provider class for plain text dictionary (Visual Assist, new IDEA dictionary format)
    DictionaryProvider class has read() and write(new_dictionary) method.
    Plain text dictionary format is EOL-separated plain text
    """

    def __init__(self, file_path, read_only=False):
        """
        Open plain text dictionary file
        :param file_path: Relative or absolute path to file
        :raise: RuntimeError if file does not exist
        """
        super(PlaintextDictionaryProvider, self).__init__(file_path, read_only)
        self.text_dictionary = []
        with open(self.path(), encoding="utf-8") as f:
            self.text_dictionary = [item.strip() for item in f.readlines()]

    def read(self):
        """
        :return: list of dictionary items
        """
        return self.text_dictionary

    def write(self, new_dictionary):
        """
        :param new_dictionary: New dictionary to write, normally merged from different sources
        """
        if self.read_only:
            logger.warning("Read-only dictionary, skip writing")
            return

        with open(self.path(), "w", encoding="utf-8") as plaintext_dict:
            plaintext_dict.write("\n".join(new_dictionary))
