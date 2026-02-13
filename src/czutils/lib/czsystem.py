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

import logging
import subprocess
import sys
from pathlib import Path


_logger = logging.getLogger(__name__)


def appName() -> str:
    """
    :return: the basename of the command that started the running application.
    """
    if len(sys.argv):
        return Path(sys.argv[0]).name
    else:
        return ""
    #else
#appName


def isProperDir(directory: str|Path):
    """
    :param directory: path to a directory

    :return: True iff directory is an actual directory, and not just a
             soft link to a directory.
    """
    directory = Path(directory)
    return directory.is_dir() and not directory.is_symlink()
#_isProperDir


def isHidden(path: str|Path) -> bool:
    """
    :return: True if the filename given by path is hidden (i.e. the base name
             starts with dot.
    """
    if isinstance(path, str) and path == "":
        raise ValueError
    #if

    return Path(path).name.startswith(".")
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
