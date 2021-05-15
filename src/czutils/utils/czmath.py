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
Mathematics library.
"""

_arabic2romanMap = (
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I')
)

def arabic2roman(n: int) -> str:
    """
    Returns the roman numeral representation of an integer.

    :param n: An integer > 0.

    :raises: ValueError
    """
    if n <= 0:
        raise ValueError("'n' must be > 0")
    #if
    ans = []
    for arabic, roman in _arabic2romanMap:
        while arabic <= n:
            ans.append(roman)
            n -= arabic
        #while
    #for
    return ''.join(ans)
#arabic2roman



### aczutro ###################################################################
