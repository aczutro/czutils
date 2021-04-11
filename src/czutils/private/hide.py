# Copyright (C) 2005 - present  Alexander Czutro <github@czutro.ch>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# For more details, see the provided licence file or
# <http://www.gnu.org/licenses>.
#
################################################################### aczutro ###

"""
"Private" help classes and functions used by module app.hide.
"""

from . import __version__, __author__

from ..utils import czcode

import argparse


def nop(*args):
    """Does nothing."""
    pass
#nop


class Breaker(Exception):
    """
    Raised to jump out of deep loops.
    """
    pass
#Breaker


@czcode.autoStr
class Flags:
    """
    Data structure that holds all flags needed by hideUnhide(...).
    """
    def __init__(self):
        self.hide = None
        self.copy = False
        self.strict = False
        self.abort = False
        self.noOverwrite = False
        self.verbose = False
    # __init__
#Flags


class CommandLineParser:
    """
    Base class for command line parsing.
    """
    def __init__(self):
        self.hideMode = None
        self.appDescription = ""
        self.helpArgs = ""
        self.helpCopy = ""
        self.helpStrict = ""
        self.helpAbort = "Abort on first failure."
        self.helpOverwrite = "Overwrite mode: if a file with the target name " \
                             "already exists, overwrite it without warning. " \
                             "Does not apply to directories."
        self.helpVerbose = "Be verbose."
    # __init__

    def parseCommandLine(self):
        """
        Parses command line.

        :return: tuple: ( list of files, Flags object )
        """
        P = argparse.ArgumentParser(description=self.appDescription,
                                    add_help=True)
        versionString = "%%(prog)s %s" % __version__
        P.add_argument("--version",
                       action="version",
                       version=versionString
                       )
        P.add_argument("FILE",
                       type=str,
                       nargs='+',
                       help=self.helpArgs
                       )
        P.add_argument("-c",
                       dest="copy",
                       action="store_true",
                       help=self.helpCopy
                       )
        P.add_argument("-s",
                       dest="strict",
                       action="store_true",
                       help=self.helpStrict
                       )
        P.add_argument("-a",
                       dest="abort",
                       action="store_true",
                       help=self.helpAbort
                       )
        P.add_argument("-o",
                       dest="noOverwrite",
                       action="store_false",
                       help=self.helpOverwrite
                       )
        P.add_argument("-v",
                       dest="verbose",
                       action="store_true",
                       help=self.helpVerbose
                       )

        container = P.parse_args()

        flags = Flags()
        flags.hide = self.hideMode
        flags.copy = container.copy
        flags.strict = container.strict
        flags.abort = container.abort
        flags.noOverwrite = container.noOverwrite
        flags.verbose = container.verbose

        return container.FILE, flags

    #def parse_args

# CommandLineParser


class CLPHide(CommandLineParser):
    """
    Command line parser for mainHide(...).
    """
    def __init__(self):
        super().__init__()
        self.hideMode = True
        self.appDescription = "Prepends a dot to the basename of each " \
                              "file/directory/symlink."
        self.helpArgs = "File/directory/symlink to hide."
        self.helpCopy = "Instead of hiding the file, make a hidden copy of it."
        self.helpStrict = "Be strict, i.e. fail if the file is already hidden. " \
                          "Otherwise, prepend a dot to the file's name in any " \
                          "case, i.e. the file name may end up having multiple dots."
    #__init__

#CLPHide


class CLPUhide(CommandLineParser):
    """
    Command line parser for mainUhide(...).
    """
    def __init__(self):
        super().__init__()
        self.hideMode = False
        self.appDescription = "Removes the prefix dot from the basename of each " \
                              "file/directory/symlink."
        self.helpArgs = 'File/directory/symlink to "unhide".'
        self.helpCopy = "Instead of unhiding the file, make an unhidden copy of it."
        self.helpStrict = "Be strict, i.e. unhide the file in any case, " \
                          "i.e. remove all prefix dots from the file name. " \
                          "Otherwise, remove only one dot."
    #__init__

#CLPUhide


### aczutro ###################################################################
