import os
import sys
import stat
import platform


PYTHON = "python3"
HOOK_CONTENT = """#!/bin/sh
#
# This file should be located in '.git/hooks' directory
# Python version depends on system, on Linux/Mac it could be 'python3'

echo "$PWD"
echo "$PWD/{relative_path}"

if command -v python3
then
    python3 "$PWD/{relative_path}"
    exit
fi

if command -v python
then
    python "$PWD/{relative_path}"
    exit
fi

"""


def is_linux():
    """
    :return: True if system is Linux, False otherwise
    """
    return platform.system() == 'Linux'


def is_macos():
    """
    :return: True if system is macOS, False otherwise
    """
    return platform.system() == 'Darwin'


def is_windows():
    """
    :return: True if system is Windows, False otherwise
    """
    return platform.system() == 'Windows'


if is_macos() or is_linux():
    PYTHON = "python3"
elif is_windows():
    PYTHON = "python"


def create_commit_hook(project_dir):
    """
    Create file 'pre-commit' in directory '{project_dir}/.git/hooks'
    :return: system return code
    """
    if not os.path.exists(project_dir):
        print("Project directory does not exist")
        return 1

    # Check '{project_dir}/.git/hooks' exist
    project_git_hooks = os.path.join(project_dir, '.git', 'hooks')
    print(f"Project git hooks directory: {project_git_hooks}")
    if not os.path.isdir(project_git_hooks):
        print(f"Directory '{project_git_hooks}' not found")
        sys.exit(1)

    # exit if hooks directory does not exist
    # TODO: instead of 'hooks' use 'dict_merge' directory
    project_hooks = os.path.join(project_dir, 'hooks')
    print(f"Project hooks directory: {project_hooks}")
    if not os.path.isdir(project_hooks):
        print(f"Directory '{project_hooks}' not found, exiting")
        sys.exit(1)

    # Create 'pre-commit' file in '{project_dir}/.git/hooks'
    pre_commit_path = os.path.join(project_git_hooks, 'pre-commit')
    print(f"Create file '{pre_commit_path}'")
    if os.path.isfile(pre_commit_path):
        print(f"File '{pre_commit_path}' already exists, removing")
        os.remove(pre_commit_path)

    # Create relative path hooks/hook_dict.py
    relative_path = os.path.join('hooks', 'dictionary_merge.py')

    # Create content of 'pre-commit' file
    with open(pre_commit_path, 'w') as pre_commit:
        pre_commit.write(HOOK_CONTENT.format(relative_path=relative_path))

    # Set file permissions to 755
    if is_linux() or is_macos():
        st = os.stat(pre_commit_path)
        os.chmod(pre_commit_path, st.st_mode | stat.S_IEXEC)


def main():
    """
    :return: System return code
    """
    if len(sys.argv) < 2:
        print("Usage: python install_hook.py <project_dir>")
        return 1
    project_dir = os.path.abspath(sys.argv[1])
    print("Project directory: %s" % project_dir)
    create_commit_hook(project_dir)
    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
