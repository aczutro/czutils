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

"""Help functions related to the (operating) system."""

from .czlogging import *
import os
import os.path
import sys


_logger = LoggingChannel("czutils.utils.czsystem",
                         LoggingLevel.SILENT,
                         colour=True)

def setLoggingOptions(level: int, colour = True) -> None:
    """
    Sets this module's logging level.  If not called, the logging level is
    SILENT.

    :param level: One of the following:
                  - czlogging.LoggingLevel.INFO
                  - czlogging.LoggingLevel.WARNING
                  - czlogging.LoggingLevel.ERROR
                  - czlogging.LoggingLevel.SILENT

    :param colour: If true, use colour in log headers.
    """
    global _logger
    _logger = LoggingChannel("czutils.utils.czsystem", level, colour=colour)

#setLoggingOptions


def appName() -> str:
    """
    :return: the basename of the command that started the running application.
    """
    if len(sys.argv):
        return os.path.basename(sys.argv[0])
    else:
        return None
    #else
#appName


def isProperDir(directory: str):
    """
    :param directory: path to a directory

    :return: True iff directory is an actual directory, and not just a
             soft link to a directory.
    """
    return os.path.isdir(directory) and not os.path.islink(directory)
#_isProperDir


def resolveAbsPath(inputPath: str) -> str:
    """
    Returns an absolute path version of inputPath.
    If inputPath is an absolute path, returns inputPath.
    Else, interprets inputPath relative to ${HOME}.
    If the HOME environment variable is not defined, interprets inputPath
    relative to the current working directory.
    """
    inputPath = os.path.normpath(inputPath)

    if inputPath == os.path.abspath(inputPath):
        return inputPath
    #if

    try:
        home = os.environ["HOME"]
    except KeyError:
        _logger.warning("environment variable HOME not defined")
        home = os.path.abspath(os.path.curdir)
    #except

    return os.path.join(home, inputPath)

#resolveFileLocation


### aczutro ###################################################################
