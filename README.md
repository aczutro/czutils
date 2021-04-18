# czutils

A "universal"  Python library  and collection  of useful  command line
utilities.

Copyright (C) 2005 - present  Alexander Czutro <github@czutro.ch>

This program is  free software: you can redistribute  it and/or modify
it under the  terms of the GNU General Public  License as published by
the Free Software Foundation, either version  3 of the License, or (at
your option) any later version.

For more details, see the provided licence file or
<http://www.gnu.org/licenses>.


## Description

This  package  comprises a  Python  library  with various  basic  help
functions and classes,  for example for automatic  code generation and
logging.

It also  a includes a  collection of useful one-task  applications for
the Unix-like command line.  These applications are designed such that
their core functionality is implemented  in the library instead of the
"main  method".  That  means that  their functionality  can easily  be
integrated into other Python applications.


## The library

The library has the following structure:

```
czutils
|-- utils            : BASIC LIBRARY PACKAGE
|   |-- czcode.py      : help functions for code automation
|   |-- czlogging.py   : a custom wrapper class for the system logger
|   `-- czsystem.py    : help functions related to the system
|-- app              : APPLICATION PACKAGE
|   |-- czmake.py      : function to create Makefiles
|   `-- hide.py        : functions to hide/unhide files
`-- private          : PRIVATE PACKAGE
```

The **basic  library package**  is the main  "public" library.   It is
intended for the integration into other libraries and applications.

The **application  package** comprises  the functionality  that powers
the  command  line  applications.   That  functionality  can  also  be
integrated into external applications or libraries.

The **private package** comprises help functions and classes needed by
the application  package.  It  is not intended  for public  use.  (But
you're welcome to browse what's in there.)


## The command line applications

### hide/uhide

These two  utilities are  for Unix-like  operating systems.   Such OSs
treat files  whose name starts with  a dot as hidden.   **hide** hides
given  files, directories  or symbolic  links by  prepending a  dot to
their name.  **uhide** "unhides" them by removing the dot.

For  example, `hide  path/to/file.txt` executes  the rename  operation
`path/to/file.txt` --> `path/to/.file.txt`, and `uhide
path/to/.file.txt` does `path/to/.file.txt` --> `path/to/file.txt`.

Both applications  are *safe*,  i.e. you  won't overwrite  anything by
accident.  However, option `-o` allows it if that's what you want.

Finally,  there  is also  a  **copy  mode**.   For example,  `hide  -c
path/to/file.txt`   will  *copy*   the   file  `path/to/file.txt`   to
`path/to/.file.txt`.   This  is  useful  for  the  creation  of  quick
back-ups (if  you don't  want to  set up a  Git repository).   In this
example, if you do something to file `path/to/file.txt` that you don't
like, you can revert the changes by copying the hidden back-up back to
the original file: `uhide -o path/to/.file.txt`.

### czmake

Reads a  plain list of shell  commands either from file  or from STDIN
and  creates a  `Makefile`  in  which each  command  is an  individual
target.

All targets are invoked by the *all* target, so a call to `make [all]`
will execute all  commands and create an individual log  file for each
command.   The `Makefile`  is formulated  such that  a second  call to
`make` will execute only the commands that failed the first time.

The `Makefile`  also includes  a *clean* target  that will  remove the
original input file, the `Makefile` itself, and all the log files.


## Installation

### The quick and dirty way

Change into  the root directory  of this distribution (where  the file
`pyproject.toml` is) and run the following command:

```shell
pip install .
```

This will install  the library **czutils** at a  location where python
will  find it,  independently of  which directory  you're in  when you
invoke python.

To access the functionality of the library from within the interactive
Python console or another Python application, import it with

```python
import czutils
```

and read the documentation with `help(czutils)`.

Pip will also install the following executable scripts:

* `hide`
* `uhide`
* `czmake`

If you  are not root when  you run the installation  command, Pip will
install the library and executables locally in your home.

To undo the installation, simply do:

```shell
pip uninstall czutils
```

### The manual way

1. Copy or move the directory  `src/czutils` to any location you like,
   for example `$HOME/python/czutils`.

2. Continuing with this example, add `$HOME/python` to the environment
   variable `PYTHONPATH`.

3. Copy  or  move  the  executable scripts  located  in  `bin` to  any
   location you like, for example `$HOME/bin`.
   
4. Make sure that `$HOME/bin` is in your `PATH` variable.


## Changelog

### Version 1.0.0: first release

#### Non-breaking additions

* new modules **utils.czcode**, **utils.czlogging** and **utils.czutils**
* new module **app.hide**
* new application scripts **hide** and **uhide**

### Version 1.1.0

#### Non-breaking additions

* new module **app.czmake**
* new application script **czmake**
