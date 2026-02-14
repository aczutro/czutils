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

"""Demo of module 'lib.cztext'."""

from ..lib import czoutline, cztext


def demo():
    """
    Demo of module 'lib.cztext'.
    """
    OL = czoutline.Outliner(h2Style=czoutline.Style.BOLD,
                            h3Style=czoutline.Style.BOLD)

    OL << """* cztext demo

             Module 'cztext' provides functions to format text that will be
             displayed on a purely text-based medium, like the
             command line terminal or the text editor.

             ** cztext.colourise

             This function takes a string and returns a copy of it with ANSI
             escape codes that will make the text and its background have the
             chosen colours when printed on ANSI-compliant
             terminals.
             """

    OL << """Three colour palettes are supported.

             *** 16-colour palette
             """
    OL.verbatim(cztext.getPalette(cztext.Palette.COL16))

    OL << "*** 256-colour palette"
    OL.verbatim(cztext.getPalette(cztext.Palette.COL256))

    OL << "*** greyscale palette"
    OL.verbatim(cztext.getPalette(cztext.Palette.GREYSCALE))

    OL << """<<
             In addition, this function can manipulate several font properties:
             >>"""

    OL.verbatim([ cztext.colourise("This is bold text.", bold=True),
                  cztext.colourise("This is slanted text.", italics=True),
                  cztext.colourise("This is underlined text.", underline=True),
                  cztext.colourise("This is struck-through text.", strikethrough=True),
                  cztext.colourise("This is blinking text.", blinking=True),
                  cztext.colourise("Here, foreground and background colours are "
                                   "inverted.", inverted=True),
                  cztext.colourise("These properties can also be combined.",
                                   bold=True,
                                   italics=True,
                                   underline=True)
                  ])

    text = """It was seven o'clock of a very warm evening
 in the Seeonee hills
      when Father Wolf woke up from his day's rest,
              scratched himself, yawned, and spread out \t his
paws one  after   the    other to get rid of the\tsleepy
                       feeling in their tips. \t"""

    OL << """** cztext.align

             This function aligns text left, right or centre:

             Take, for example, this input text:

             >>
             """
    OL.verbatim(text)

    OL << "*** aligned left"
    OL.verbatim(cztext.align(text.splitlines(), 'l', collapseSpaces=True))

    OL << "*** aligned right"
    OL.verbatim(cztext.align(text.splitlines(), 'r', collapseSpaces=True))

    OL << "*** centered"
    OL.verbatim(cztext.align(text.splitlines(), 'c', collapseSpaces=True))

    OL << """** cztext.fill

             This function fills up all lines without exceeding a maximum line
             width.  For example:
             >>
             """

    l = lambda _b, _f, _w : [ cztext.colourise(line.ljust(_w),
                                               background=_b,
                                               foreground=_f,
                                               palette=cztext.Palette.COL256
                                               )
                              for line in cztext.fill(text, _w) ]

    OL.verbatim(l(229, 202, 60))
    OL.verbatim(l(195, 27, 40))
    OL.verbatim(l(194, 22, 20))
#demo


### aczutro ###################################################################
