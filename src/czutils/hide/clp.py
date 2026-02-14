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
Command line parser for 'hide' and 'uhide'.
"""
from .. import __version__

import argparse
from dataclasses import dataclass
import logging

_logger = logging.getLogger(__name__)


@dataclass
class Args:
    hide:        bool
    files:       list[str]
    copy:        bool
    strict:      bool
    abort:       bool
    noOverwrite: bool
    verbose:     bool
#Args


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


    def parseCommandLine(self) -> argparse.Namespace:
        """
        Parses command line.

        :returns: All arguments and flags bundled in an Args object.
        """
        P = argparse.ArgumentParser(description=self.appDescription,
                                    add_help=True)
        P.add_argument("--version",
                       action="version",
                       version=f"czutils version {__version__}"
                       )
        P.add_argument("files",
                       metavar='FILE',
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
        setattr(container, "hide", self.hideMode)

        _logger.info(container)

        return Args(**vars(container))
    #parseCommandLine

# CommandLineParser


class CLPHide(CommandLineParser):
    """
    Command line parser for mainHide(...).
    """
    def __init__(self):
        super().__init__()
        self.hideMode = True
        self.appDescription = ("Prepends a dot to the basename of each " 
                               "file/directory/symlink."
                               )
        self.helpArgs = "File/directory/symlink to hide."
        self.helpCopy = "Instead of hiding the file, make a hidden copy of it."
        self.helpStrict = ("Be strict, i.e. fail if the file is already hidden. " 
                           "Otherwise, prepend a dot to the file's name in any " 
                           "case, i.e. the file name may end up having multiple dots."
                           )
    #__init__
#CLPHide


class CLPUhide(CommandLineParser):
    """
    Command line parser for mainUhide(...).
    """
    def __init__(self):
        super().__init__()
        self.hideMode = False
        self.appDescription = ("Removes the prefix dot from the basename of each " 
                               "file/directory/symlink."
                               )
        self.helpArgs = 'File/directory/symlink to "unhide".'
        self.helpCopy = "Instead of unhiding the file, make an unhidden copy of it."
        self.helpStrict = ("Be strict, i.e. unhide the file in any case, " 
                           "i.e. remove all prefix dots from the file name. " 
                           "Otherwise, remove only one dot."
                           )
    #__init__
#CLPUhide


### aczutro ###################################################################
