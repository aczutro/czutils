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

"""A simple system to output messages intended for the user."""

import sys
from typing import Any, Callable, TextIO


def _defaultInfoFormatter(obj: Any) -> str:
    return f"{obj}"
#_defaultInfoFormatter


def _defaultWarningFormatter(obj: Any) -> str:
    return f"Warning: {obj}"
#_defaultWarningFormatter


def _defaultErrorFormatter(obj: Any) -> str:
    return f"ERROR: {obj}"
#_defaultErrorFormatter


class OutputChannel:
    """"""

    def __init__(self):
        """"""
        self.infoChannel    : TextIO = sys.stdout
        self.warningChannel : TextIO = sys.stderr
        self.errorChannel   : TextIO = sys.stderr

        self.infoFormatter    : Callable[[str], str] = _defaultInfoFormatter
        self.warningFormatter : Callable[[str], str] = _defaultWarningFormatter
        self.errorFormatter   : Callable[[str], str] = _defaultErrorFormatter
    #__init__


    def info(self,
             obj: Any,
             newline: bool = True,
             flush: bool = True,
             ):
        """
        Produces an informational message.
        """
        self.infoChannel.write(self.infoFormatter(obj))
        if newline:
            self.infoChannel.write("\n")
        #if
        if flush:
            self.infoChannel.flush()
        #if
    #info


    def warning(self,
                obj: Any,
                newline: bool = True,
                flush: bool = True,
                ):
        """
        Produces a warning message.
        """
        self.warningChannel.write(self.warningFormatter(obj))
        if newline:
            self.warningChannel.write("\n")
        #if
        if flush:
            self.warningChannel.flush()
        #if
    #warning


    def error(self,
              obj: Any,
              newline: bool = True,
              flush: bool = True,
              ):
        """
        Produces an error message.
        """
        self.errorChannel.write(self.errorFormatter(obj))
        if newline:
            self.errorChannel.write("\n")
        #if
        if flush:
            self.errorChannel.flush()
        #if
    #error

#OutputChannel


class DumbOutputChannel(OutputChannel):
    """An OutputChannel that does nothing."""

    def info(self, *args, **kwargs):
        pass
    #info

    def warning(self, *args, **kwargs):
        pass
    #info

    def error(self, *args, **kwargs):
        pass
    #info

#DumbOutputChannel


### aczutro ###################################################################
