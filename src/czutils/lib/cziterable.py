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

"""Help functions to search in iterables."""


def findFirstOf(iterable, candidates) -> int:
    """
    Searches for the first occurrence in 'iterable' of any of the candidates in
    'candidates'.

    :param iterable:   A string, list, tuple or any iterable.
    :param candidates: A non-empty set of search items.

    :returns: Index of the first occurrence if found; -1 if not found.
    """
    if not candidates:
        raise ValueError("'candidates' must not be empty")
    #if

    index = -1
    for item in iterable:
        index += 1
        if item in candidates:
            return index
        #if
    #for

    return -1
#findFirstOf


def findFirstNotOf(iterable, blackList) -> int:
    """
    Searches for the first occurrence in 'iterable' of any item that is not
    blacklisted.

    :param iterable:  A string, list, tuple or any iterable.
    :param blackList: A non-empty set of blacklisted items.

    :returns: Index of the first occurrence if found; -1 if not found.
    """
    if not blackList:
        raise ValueError("'blackList' must not be empty")
    #if

    index = -1
    for item in iterable:
        index += 1
        if item not in blackList:
            return index
        #if
    #for

    return -1
#findFirstNotOf


def findLastOf(iterable, candidates) -> int:
    """
    Searches for the last occurrence in 'iterable' of any of the candidates in
    'candidates'.

    :param iterable:   A string, list, tuple or any iterable.
    :param candidates: A non-empty set of search items.

    :returns: Index of the last occurrence if found; -1 if not found.
    """
    if not candidates:
        raise ValueError("'candidates' must not be empty")
    #if

    index = len(iterable)
    for item in reversed(iterable):
        index -= 1
        if item in candidates:
            return index
        #if
    #for

    return -1
#findLastOf


def findLastNotOf(iterable, blackList) -> int:
    """
    Searches for the last occurrence in 'iterable' of any item that is not
    blacklisted.

    :param iterable:  A string, list, tuple or any iterable.
    :param blackList: A non-empty set of blacklisted items.

    :returns: Index of the last occurrence if found; -1 if not found.
    """
    if not blackList:
        raise ValueError("'blackList' must not be empty")
    #if

    index = len(iterable)
    for item in reversed(iterable):
        index -= 1
        if item not in blackList:
            return index
        #if
    #for

    return -1
#findLastNotOf


### aczutro ###################################################################
