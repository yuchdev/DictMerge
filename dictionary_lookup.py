import os
from log_helper import logger
from path_helper import user_name, home_dir, appdata_dir, jetbrains_appdata, SYSTEM_DICT

__doc__ = """Lookup all sorts of dictionaries"""


def files_lookup(root_folder, files_list):
    """
    Recursive lookup for files in the root folder using os.walk()
    :param root_folder: Directory root project, where from we start looking for dictionaries
    :param files_list: List of files to search
    :return: List of absolute paths to all dictionaries, including file name
    """
    dictionaries = []
    assert isinstance(root_folder, str), "Root folder must be a string, not %s" % type(root_folder)
    assert isinstance(files_list, list), "Files list must be a list, not %s" % type(files_list)
    for root, dirs, files in os.walk(root_folder):
        for file_name in files_list:
            if file_name in files:
                dictionaries.append(os.path.abspath(os.path.join(root, file_name)))
    return dictionaries


class DictionaryLookup:

    def __init__(self, projects_dir):
        self.projects_dir = projects_dir
        if not os.path.isdir(self.projects_dir):
            logger.warning("Directory %s does not exist" % self.projects_dir)
            raise FileNotFoundError("Directory %s does not exist" % self.projects_dir)

    def lookup_idea(self, dict_name=None):
        """
        Lookup IDEA dictionaries in the current project and in the AppData
        :return: list of absolute paths to IDEA dictionaries
        """
        found_dictionaries = []
        dict_name = dict_name if dict_name else user_name()
        found_dictionaries.extend(files_lookup(self.projects_dir, [f"{dict_name}.xml"]))
        found_dictionaries.extend(files_lookup(jetbrains_appdata(),
                                               ["spellchecker-dictionary.xml", "cachedDictionary.xml"]))

        logger.debug("Found following dictionaries: {}".format(found_dictionaries))
        return found_dictionaries

    def lookup_plaintext(self):
        """
        Lookup plain text dictionaries in the current dir and the AppData
        :return: list of absolute paths to plain text dictionaries
        """
        found_dictionaries = []
        found_dictionaries.extend(files_lookup(self.projects_dir, ["dictionary.dic", "UserWords.txt"]))
        found_dictionaries.extend(files_lookup(appdata_dir(), ["UserWords.txt"]))

        # Create system dictionary if not exists
        if not os.path.isfile(SYSTEM_DICT.format(homedir=home_dir())):
            with open(SYSTEM_DICT.format(homedir=home_dir()), "w") as f:
                f.write("")

        found_dictionaries.append(SYSTEM_DICT.format(homedir=home_dir()))

        logger.debug("Found following dictionaries: {}".format(found_dictionaries))
        return found_dictionaries

    def lookup(self):
        """
        Lookup all dictionaries in the current project and in the AppData
        :return: list of absolute paths to IDEA dictionaries
        """
        found_dictionaries = []
        found_dictionaries.extend(self.lookup_idea())
        found_dictionaries.extend(self.lookup_plaintext())
        return found_dictionaries

    @staticmethod
    def lookup_appdata():
        """
        Lookup all dictionaries in the AppData
        :return: list of absolute paths to IDEA dictionaries
        """
        found_dictionaries = []
        found_dictionaries.extend(files_lookup(jetbrains_appdata(),
                                               ["spellchecker-dictionary.xml", "cachedDictionary.xml"]))
        found_dictionaries.extend(files_lookup(appdata_dir(), ["UserWords.txt"]))
        return found_dictionaries
