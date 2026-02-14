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

"""Demo of module 'lib.czmath'."""

from ..lib import czmath, czoutline

import io


def demo():
    """
    Demo of module 'lib.czmath'.
    """
    OL = czoutline.Outliner(h2Style=czoutline.Style.BOLD,
                            h3Style=czoutline.Style.BOLD
                            )
    OL << """* czmath demo

          ** czmath.arabic2roman

          This function returns the roman numeral representation of an integer.
          Here are the numbers 1 to 100:
          """
    first = lambda _i: ("%d:" % _i).rjust(6)
    second = lambda _i, _w: czmath.arabic2roman(_i).ljust(_w)

    text = io.StringIO()
    for i in range(1, 26):
        print(first(i), second(i, 5),
              first(i + 25), second(i + 25, 7),
              first(i + 50), second(i + 50, 6),
              first(i + 75), second(i + 75, 8),
              file=text
              )
    #for

    OL.verbatim(text.getvalue())
#demo


### aczutro ###################################################################
