# czutils

A collection of useful command line utilities and libraries for Python 3.

Copyright (C) 2005 - present  Alexander Czutro <github@czutro.ch>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

For more details, see the provided licence file or
<http://www.gnu.org/licenses>.


## Description

This package comprises a Python 3 library with various help functions
and classes that can make code more compact and easy-to-read.

It also a includes a collection of useful one-task applications for the
Unix-like command line.  These applications are designed such that
their core functionality is implemented in the library instead of the
"main method".  That means that their functionality can easily be 
integrated into other Python applications.

## The library

The library has the following structure:

```
czutils
|-- utils
|   |-- czcode.py    : help functions for code automation
|   |-- czlogging.py : a custom wrapper class for the system logger
|   `-- czsystem.py  : help functions related to the system environment
`-- hide.py : functions to hide/unhide files
```

## Applications

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

### 1. Install the library

Change into the root directory of this distribution (where the files 
`setup.py` and `setup.cfg` are) and run the following command.  If you
are not root when you run this command, it will install the library
locally in your home (and it will be available only to you).

```python -m pip install .```

The functionality of the library can be accessed from within the 
interactive Python console or another Python application with

```python
import czutils
```

### 2. "Install" the applications

Copy or move all executables in directory `bin` to any location of
your preference (ideally one that is in your `PATH` variable).  Make
sure they are executable, or make them with `chmod +x`.  If you 
like, you may rename the main executables.
