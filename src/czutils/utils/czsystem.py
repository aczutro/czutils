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
import subprocess
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


def mkdir(path: str, p = False) -> None:
    """
    Extended version of os.mkdir which also implements the -p flag.

    :param path: directory to create
    :param p:    If true, also create parent directories if necessary.
                 Also, if true, suppresses FileExistsError if the directory
                 already exists.

    :raises: ValueError if path is empty.
    :raises: All exceptions that os.mkdir may raise, like FileExistsError,
             FileNotFoundError, PermissionError, etc
    """
    if path == "":
        raise ValueError
    #if
    if path != os.path.sep and path[-1] == os.path.sep:
        path = path[:-1]
    #if
    try:
        os.mkdir(path)
    except FileExistsError as e:
        if not (os.path.isdir(path) and p):
            raise e
        #if
    except FileNotFoundError as e:
        parent = os.path.dirname(path)
        if p and parent != path:
            mkdir(parent, p)
            mkdir(path, p)
        else:
            raise e
        #else
    #except
#mkdir


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


def filenameSplit(filename: str) -> tuple:
    """
    Splits a filename into a head (everything before the last dot) and a tail
    (the "filename extension", i.e. what comes after the last dot.
    :param filename:
    :return: tuple (head, tail)
    :raises: ValueError if filename is empty or ".".
    """
    if filename in [ "", "." ]:
        raise ValueError
    #if

    if filename[0] == '.':
        head, tail = filenameSplit(filename[1:])
        return (".%s" % head, tail)
    #if

    tokens = filename.split(sep='.')
    if len(tokens) < 2:
        return (filename, "")
    else:
        return (".".join(tokens[:-1]), tokens[-1])
    #else
#filenameSplit


def isHidden(path: str) -> bool:
    """
    :return: True if the filename given by path is hidden (i.e. the base name
             starts with dot.
    """
    if path == "":
        raise ValueError
    #if
    a, b = os.path.split(path)
    if b == "":
        a, b = os.path.split(a)
    #if
    return len(b) and b[0] == '.'
#isHidden


class SystemCallError(Exception):
    pass
#SystemCallError


class SystemCaller:
    """
    Executes sub-processes non-interactively and saves their stdout and stderr.
    """
    def __init__(self, exceptionOnFailure: bool):
        """
        :param exceptionOnFailure: If true, call() raises a SystemCallError if
                                   the sub-process fails.  Else, call() returns
                                   the sub-process's return code.
        """
        self._stdout = ""
        self._stderr = ""
        self._doRaise = exceptionOnFailure
    #__init__


    def stdout(self):
        return self._stdout
    #stdout


    def stderr(self):
        return self._stderr
    #stdout


    def call(self, args: list) -> int:
        P = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = P.communicate()
        self._stdout = stdout.decode(errors="ignore")
        self._stderr = stderr.decode(errors="ignore")
        if P.returncode:
            _logger.warning("'%s'" % " ".join(args), "returned", P.returncode)
            if self._doRaise:
                raise SystemCallError(self._stderr)
            #if
        #if
        return P.returncode
    #def

#SystemCaller


### aczutro ###################################################################
