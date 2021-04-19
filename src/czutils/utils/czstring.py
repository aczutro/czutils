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

"""String functions."""

from . import cziterable


def isStrippable(s: str, chars: str):
    """
    :param s:     A string.
    :param chars: A non-empty set of characters.

    :returns: True if s.strip(chars) would differ from s.

    :raises: ValueError
    """
    begin = cziterable.findFirstNotOf(s, chars)
    end = cziterable.findLastNotOf(s, chars)

    return (begin, end) != (0, len(s) - 1)
#isStrippable


### aczutro ###################################################################
