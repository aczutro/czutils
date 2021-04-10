# czutils
A collection of useful command line utilities and libraries for Python 3.

Copyright (C) 2005 - present  Alexander Czutro <github@czutro.ch>

Licence: GNU GPL v3

## Description

A collection of useful one-task applications for the Linux/Unix command line.

### hide/uhide

These two utilities make sense only on Unix-like systems, where the OS treats
files whose name starts with a dot as hidden.  `hide` renames all given objects
(files, directories or symbolic links) in order to hide them. `uhide` unhides
them.

Both applications accept full paths and are **safe** (i.e. you won't overwrite
anything by accident).  They also offer options that may sound strange, but
which can be useful; for example, **copy mode**, the option to "hide" hidden
files (`'/path/to/.file' -> '/path/to/..file'`), and the options to unhide
files hidden multiple times only partially (`'/path/to/...file' ->
'/path/to/..file'`) or fully (`'/path/to/...file' -> '/path/to/file'`).

For example, assume you want to apply a batch transformation to all images in
a given directory.  You can make a quick back up (without having to set
up a Git repository first) with

```shell
hide -c ./path/to/*.jpg
```

With this command, each file `./path/to/file.jpg` is copied to
`./path/to/.file.jpg`.

In the end, if you didn't like the result of the automatic colour correction
of your newest image manipulation software, simply revert your changes, by
unhiding your back ups and overriding the files you don't like:

```shell
uhide -o ./path/to/.*.jpg
```

With this, each file `./path/to/file.jpg` will be replaced by its backup
`./path/to/.file.jpg`.


## Installation

1. Change into the root directory of this distribution (where the files 
   `setup.py` and `setup.cfg` are) and run the following command.  You
   don't need to be root to do it.

```python -m pip install .```

2. Copy or move all main executables in directory `bin` to any location of
   your preference (ideally one that is in your `PATH` variable).  If you 
   like, you may rename the main executables.
   
After the first step, the library's functionality will also be available in
the interactive Python console with

```python
import czutils
```
