import os
import sys
import argparse
from dictionary_lookup import user_name, DictionaryLookup
from dictionary_provider import IdeaDictionaryProvider, PlaintextDictionaryProvider
from path_helper import projects_dir
from log_helper import logger


def merge_dictionaries(all_dictionaries) -> list:
    """
    :param all_dictionaries: a number of dictionaries of different types
    :return: union of dictionaries content
    """
    merged_set = set()
    for dictionary in all_dictionaries:
        new_dictionary = set(dictionary.read())
        logger.info("Size of appended dictionary [%s] is %d words" % (dictionary.name(), len(new_dictionary)))
        merged_set = merged_set.union(new_dictionary)
    return sorted(merged_set)


def main():
    """
    Merge dictionaries using provided command-line params.
    :return: System return code
    """
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--idea-dictionary',
                        help='Add XML-based IDEA dictionary as a merge source',
                        action='append',
                        dest='idea_dictionary',
                        required=False,
                        default=[])
    parser.add_argument('--plaintext-dictionary',
                        help='Add plain text dictionary (VisualStudio, new IDEA, and many others) as a merge source',
                        action='append',
                        dest='text_dictionary',
                        required=False,
                        default=[])
    parser.add_argument('--lookup-directory',
                        help='Lookup directory for IDEA and text dictionaries',
                        required=False,
                        default=projects_dir())
    parser.add_argument('--idea-dictionary-name',
                        help='Name of IDEA dictionary to lookup',
                        required=False,
                        default=user_name())

    args = parser.parse_args()
    assert isinstance(args.idea_dictionary, list)
    assert isinstance(args.text_dictionary, list)
    assert isinstance(args.lookup_directory, str)
    all_dictionaries = []

    for idea_xml_file in args.idea_dictionary:
        idea_dict_path = os.path.abspath(idea_xml_file)
        logger.info("User IDEA dictionary file: %s" % idea_dict_path)
        if not os.path.isfile(idea_dict_path):
            logger.warning("%s IDEA dict not found" % idea_dict_path)
            return 1
        if os.stat(idea_dict_path).st_size == 0:
            logger.warning("%s IDEA dict has zero size" % idea_dict_path)
            return 1
        idea_dict = IdeaDictionaryProvider(idea_dict_path)
        all_dictionaries.append(idea_dict)

    for text_file in args.text_dictionary:
        plaintext_file_path = os.path.abspath(text_file)
        logger.info("User plaintext dictionary file: %s" % plaintext_file_path)
        if not os.path.isfile(plaintext_file_path):
            logger.warning("%s plaintext dict not found" % plaintext_file_path)
            return 1
        if os.stat(plaintext_file_path).st_size == 0:
            logger.warning("%s plaintext dict has zero size" % plaintext_file_path)
            return 1
        plaintext_dict = PlaintextDictionaryProvider(plaintext_file_path)
        all_dictionaries.append(plaintext_dict)

    logger.info("%d dictionaries to merge" % len(all_dictionaries))

    if args.lookup_directory:
        lookup_dir = os.path.abspath(args.lookup_directory)
        logger.info("Lookup directory: %s" % lookup_dir)
        dict_lookup = DictionaryLookup(projects_dir=lookup_dir)
        for plaintext_dict in dict_lookup.lookup_plaintext():
            all_dictionaries.append(PlaintextDictionaryProvider(plaintext_dict))
        for idea_dict in dict_lookup.lookup_idea(dict_name=args.idea_dictionary_name):
            all_dictionaries.append(IdeaDictionaryProvider(idea_dict))
    else:
        logger.info("Lookup directory not specified, lookup AppData only")
        all_dictionaries.append(DictionaryLookup.lookup_appdata())

    if len(all_dictionaries) < 2:
        logger.info("Only %d dictionaries has been found, nothing to merge" % len(all_dictionaries))
        return 0

    # Merge contents of all dictionaries
    merged_dictionary = merge_dictionaries(all_dictionaries)
    logger.info("Merge complete, size of resulting dictionary is %d words" % len(merged_dictionary))

    # Write merged dictionary to all IDEA and plaintext dictionaries
    for dictionary in all_dictionaries:
        logger.info("Write merged dictionary to %s" % dictionary.name())
        dictionary.write(merged_dictionary)

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
