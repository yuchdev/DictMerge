import os
import platform
from log_helper import logger

__doc__ = """Paths to JetBrains AppData, $HOME, $USER, and temporary dictionaries"""

SYSTEM_DICT = "{homedir}/.idea/dictionaries/dictionary.dic"
MACOS_APPDATA = "{homedir}/Library/Application Support"
WINDOWS_APPDATA = "{homedir}/AppData/Roaming"
JETBRAINS_APPDATA = "{appdata}/JetBrains"


def environment_value(environment_name):
    """
    :param environment_name: Name of the environment variable
    :return: Value of the environment variable or the empty string if not exists
    """
    try:
        return os.environ[environment_name]
    except KeyError:
        return ''


def user_name():
    """
    :return: Cross-platform username of the current user
    """
    if platform.system() == "Windows":
        return environment_value("USERNAME")
    else:
        return environment_value("USER")


def home_dir():
    """
    :return: Home directory of the current user
    """
    if platform.system() == "Windows":
        return environment_value("USERPROFILE")
    elif platform.system() == "Darwin":
        return environment_value("HOME")
    else:
        return environment_value("HOME")


def appdata_dir():
    """
    :return: AppData directory of the current user depend on system
    """
    if platform.system() == "Windows":
        return WINDOWS_APPDATA.format(homedir=home_dir())
    elif platform.system() == "Darwin":
        return MACOS_APPDATA.format(homedir=home_dir())
    else:
        return home_dir()


def jetbrains_appdata():
    """
    Find all temporary dictionaries in JetBrains AppData dir
    :return:
    """
    jb_appdata = JETBRAINS_APPDATA.format(appdata=appdata_dir())
    if not os.path.isdir(jb_appdata):
        logger.warning("JetBrains AppData directory %s is not found, exiting hook" % jb_appdata)
        return []
    logger.info("JetBrains AppData dir: %s" % jb_appdata)
    return jb_appdata


def projects_dir():
    """
    :return: $PROJECTS dir is defines
    """
    return environment_value("PROJECTS")
