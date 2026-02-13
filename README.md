# czutils

A "universal" Python library and a collection of useful command line utilities.

Copyright (C) 2005 - present  Alexander Czutro <github@czutro.ch>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public Licence as published by the Free Software
Foundation, either version 3 of the Licence or (at your option) any later
version.

For more details, see the provided licence file or
<http://www.gnu.org/licenses>.


## Description

This package comprises a "universal" Python library meant to extend the Python
Standard Library.  In addition, it comprises a set of command-line utilities
created according to the Unix philosophy of having a small separate utility for
each task.  Each utility can do only one thing, but it does that one thing well
and efficiently.  These are handy helpers for people who prefer to manage their
files using the command line instead of a graphical front-end.


### The universal library

The **universal library** is implemented in subpackage `lib`.  The following
modules are currently available:

|               |                                                                           |
|--------------:|:--------------------------------------------------------------------------|
|      `czcode` | Help functions for code generation.                                       |
|  `cziterable` | Generic functions to search in iterables.                                 |
|  `czuioutput` | A simple system to output messages intended for the user.                 |
|      `czmath` | Mathematics library.                                                      |
|   `czoutline` | A document formatter for text displayed on a monospace-text-based medium. |
|  `czstrutils` | String manipulation functions.                                            |
|    `czsystem` | Help functions related to the (operating) system.                         |
|      `cztext` | Functions to format long texts and to colourise strings.                  |
| `czthreading` | Base classes for asynchronous components that run in their own thread.    |
|      `cztime` | An easy-to-use timer.                                                     |

The command-line application `czutils-demo` provides usage examples.


### The application library

The following table lists the currently available applications.  The first
column lists the application names for command-line use, and the second column
lists the corresponding module for integration into Python applications.

|                |              |                                                            |
|---------------:|-------------:|:-----------------------------------------------------------|
| `czutils-demo` |       `demo` | Demo application to illustrate the library's capabilities. |
|       `czmake` |     `czmake` | Turns a plain list of commands into a Makefile.            |
|         `hide` |       `hide` | Hides files (prepends a dot to their names).               |
|        `uhide` |       `hide` | "Unhides" files (removes leading dots from their names).   |
|   `textformat` | `textformat` | Formats text-based documents for display on the terminal.  |

All applications provide help when invoked with the `--help` option.  Some also
provide a `--long-help` option which produces output similar to a manpage.


## Changelog

### Version 1.0.0: first release

#### Non-breaking

* new modules **utils.czcode**, **utils.czlogging** and **utils.czutils**
* new module **app.hide**
* new application scripts **hide** and **uhide**

### Version 1.1.0

#### Non-breaking

* new module **app.czmake**
* new application script **czmake**

### Version 1.2.0

#### Non-breaking

* new modules **utils.cziterable**, **utils.czstring** and **utils.cztime**
* new module **app.fill**
* new application script **fill**
* **czmake** now reads from STDIN also if no '-' is given.

### Version 1.3.0

#### Breaking

* module **utils.czstring** removed
* module **app.fill** removed (functionality migrated to new modules
  **utils.czoutline**, **utils.cztext** and **app.textformat**)
* command-line application **fill** renamed to **textformat** (with extended
  functionality)

#### Non-breaking

* new modules **utils.czoutline** and **utils.cztext**
* new command-line applications **textformat** and **czutils-demo**

### Version 1.4.0

#### Breaking

* **czlogging.LogLevel** renamed to **czlogging.LoggingLevel**
* **czlogging.LogChannel** renamed to **czlogging.LoggingChannel**

#### Non-breaking

* new logging level **SILENT**
* now each LoggingChannel instance can have its own logging level
* support for colour output in logging messages
* new demo: **czlogging**
* new module **utils.czthreading**
* **czsystem**: new function **resolveAbsPath**
* Modules **czthreading** and **czsystem** define a module-wide logger
  (LoggingChannel instance), and provide function **setLoggingOptions** to
  change the module's logging level.

### Version 1.4.1

#### Non-breaking

* new module **czstrutils** with function **grep**
* new functions **filenameSplit** and **isHidden** in module **czsystem**
* new class **SystemCaller** in module **czsystem**

### Version 1.5.0

* Breaking: removed module **czlogging**.
* New module **czuioutput**.
