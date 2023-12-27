# Copyright (C) 2023 - present  Alexander Czutro <github@czutro.ch>
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

"""String manipulation utilities."""

from .czlogging import *
from .cztext import *
import re


_logger = LoggingChannel("czutils.utils.czstrutils",
                         LoggingLevel.SILENT,
                         colour=True)

def setLoggingOptions(level: int, colour=True) -> None:
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
    _logger = LoggingChannel("czutils.utils.czstrutils", level, colour=colour)
#setLoggingOptions


def grep(pattern: str, text, ignoreCase=False, colour=False) -> list:
    """
    Searches for pattern in text.

    :param pattern:    search pattern, may contain Python regular expressions
                       (re module).
    :param text:       The input text, either a single string with newline
                       characters, or a list of strings without newline
                       characters.  In the latter case, each string in the list
                       is a line.
    :param ignoreCase: If true, do case-insensitive search.
    :param colour:     If true, colourise the match.

    :return: List of strings, where each string is a matching line.
    """
    if type(text) is str:
        return grep(pattern, text.split(sep='\n'), ignoreCase, colour)
    #if

    flags = re.IGNORECASE if ignoreCase else 0
    matcher = re.compile(pattern, flags)
    ans = []
    for line in text:
        if colour:
            match = matcher.search(line)
            if match is not None:
                start, end = match.start(), match.end()
                ans.append("%s%s%s"
                           % (line[:start],
                              colourise(line[start:end], Col16.RED, bold=True),
                              line[end:]))
            #if
        else:
            if matcher.search(line) is not None:
                ans.append(line)
            #if
        #else
    #for
    return ans
#grep


### aczutro ###################################################################
