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

This package comprises a Python 3 library with various basic help
functions and classes, for example for automatic code generation and
logging.

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
files whose name starts with a dot as hidden.  **hide** hides all given 
objects (files, directories or symbolic links) by prepending a dot to their
name.  **uhide** "unhides" them by removing the dot.

For example, `hide path/to/file.txt` does the rename operation
`path/to/file.txt` --> `path/to/.file.txt`, and `uhide path/to/.file.txt` does
`path/to/.file.txt` --> `path/to/file.txt`.

Both applications are *safe*, i.e. you won't overwrite anything by accident.
However, option `-o` allows it if that's what you want.

Finally, there is also a **copy mode**.  For example,
`hide -c path/to/file.txt` will *copy* the file `path/to/file.txt` to
`path/to/.file.txt`.  This is useful for the creation of quick back-ups (if
you don't want to set up a Git repository).  In this example, if you do
something to file `path/to/file.txt` that you don't like, you can apply the
back-up with `uhide -o path/to/.file.txt`.


## Installation

### 1. Install the library

Change into the root directory of this distribution (where the files 
`setup.py` and `setup.cfg` are) and run the following command:

```python -m pip install .```

(If you are not root when you run this command, it will install the library
locally in your home, but it will be available only to you.)

After the installation, the functionality of the library can be accessed
from within the interactive Python console or another Python application
with

```python
import czutils
```

Use `help(czutils)` to access the documentation included in the code.

### 2. "Install" the applications

Copy or move the executables in directory `bin` to any location of
your preference (ideally one that is in your `PATH` variable).  
If you like, you may rename them.


## Changelog

### Version 1.0: first release

#### Non-breaking additions

* new package **utils** with modules **czcode**, **czlogging** and
  **czutils**
* new module **hide**
* new applications **hide** and **uhide**
