# Dictionary Merge

We work with a number of different tools (IDEs, editors, etc.) 
that use different formats for storing dictionaries (plain text, XML, JSON, YAML)
Normally, you have to add a single word to each dictionary, while working with your IDEs and editors.  
This tool allows you to merge dictionaries of different formats into a single dictionary.

It can perform lookup of the dictionaries in the specific directory,
lookup for dictionaries in the temporary and configuration directories like `AppData`, `.config`, etc.,
knows special dictionary names and locations, like IDEA's `spellchecker-dictionary.xml`. 

## Usecases

### Merge two specific plain-text dictionaries

```bash
python dictionary_merge.py --plaintext-dictionary VisualAssist/Dict/UserWords.txt --plaintext-dictionary idea.dic
```

### Merge two specific dictionaries of different formats

```bash
python dictionary_merge.py --idea-dictionary spellchecker-dictionary.xml --plaintext-dictionary idea.dic
```

### Merge all dictionaries in the directory

```bash
python dictionary_merge.py --lookup-directory ~/Projects/MyProject
```

### Merge dictionaries at every commit

Sometimes you want to merge dictionaries at every commit. You can do it with the help of `pre-commit` Git hook.
The Python script `install_hook.py` will install the hook for you, set the relative path, and correct file permissions.

```bash
git config --global core.hooksPath .githooks
python install_hook.py
```

## Setup for manual use

* Install Python 3.6+
* Set the environment variable `PROJECTS` pointing to the directory where your projects are located (usually `$HOME/Projects`)

## Setup as a git hook

* add the project as your Git submodule: `git submodule add https://github.com/yuchdev/DictMerge.git .githooks/DictMerge`
* install the hook: `python .githooks/DictMerge/install_hook.py`
* the merge process will be executed at every commit
