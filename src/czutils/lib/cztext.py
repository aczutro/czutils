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

"""Functions to format long texts and to colourise strings."""

import itertools
import re


_BLANKS = " \t\f\v\r\n"


def paragraphy(text: str | list[str] | tuple[str]) -> list:
    """
    Splits text into paragraphs.  Detects paragraph breaks by searching for
    empty lines.  Does not produce empty paragraphs.  I.e., e.g., that
    "a\n\n\n\nb" becomes ["a", "b"].

    :param text: May be a single string or a list of strings.  If the latter,
                 'paragraphy' assumes that each string in the list is a line
                 containing no newline characters.

    :returns: A list of strings where each string is a paragraph.

    :raises: TypeError
    """
    if not text:
        return []
    #if

    if isinstance(text, str):
        return paragraphy(text.strip(_BLANKS).splitlines())

    elif isinstance(text, list) or isinstance(text, tuple):
        ans = []
        N = len(text)
        begin = 0
        for i in range(N):
            text[i] = text[i].strip(_BLANKS)
            if not text[i]:
                if i != begin:
                    ans.append(' '.join(text[begin:i]))
                #if
                begin = i + 1
            #if
        #for
        if N != begin:
            ans.append(' '.join(text[begin:N]))
        #if
        return ans

    else:
        raise TypeError("'text' must be string or a list of strings")
    #else
#paragraphy


def fill(text: str | list[str] | tuple[str],
         lineWidth : int,
         ) -> list:
    """
    Reformats the input text so that all lines are filled with a maximum length
    of 'lineWidth' characters.  Makes sure that all periods that end a sentence
    are followed by 2 spaces, and replaces all other space clusters (that
    includes tabs) by single spaces.

    :param text:      Input text is treated like a single paragraph.  If in
                      doubt, split your text into paragraphs with 'paragraphy'.
                      May be a single string, or a list of strings.  If the
                      latter, 'fill' assumes that each string in the list is a
                      line containing no newline characters.

    :param lineWidth: the maximum number of characters each line may have.  The
                      maximum line length is guaranteed unless the input text
                      contains individual words longer than lineWidth.
                      Must be > 9.

    :return: A list of strings where each string is a non-newline-terminated
             line.

    :raises: TypeError, ValueError
    """
    tokenise = lambda s : re.split("[ \t\f\v\r\n]+", s.strip(_BLANKS))

    if isinstance(text, str):
        tokens = tokenise(text)
    elif isinstance(text, list) or isinstance(text, tuple):
        tokens = list(itertools.chain.from_iterable(
            [ tokenise(s) for s in text if s.strip(_BLANKS) ]))
    else:
        raise TypeError("'text' must be a string or a list of strings")
    #else

    if lineWidth < 10:
        raise ValueError("'lineWidth' must be > 9")
    #if

    slices = []
    length = -1
    for i in range(len(tokens)):

        period = False
        if tokens[i].endswith('.'):
            period = True
            tokens[i] += ' '
        #if

        newLength = length + len(tokens[i]) + 1

        if newLength < lineWidth:
            length = newLength
        elif newLength == lineWidth or (period and newLength == (lineWidth + 1)):
            slices.append(i + 1)
            if period:
                tokens[i] = tokens[i][:-1]
            #if
            length = -1
        else:
            slices.append(i)
            length = len(tokens[i])
        #else
    #for

    if not slices or slices[-1] != len(tokens):
        slices.append(len(tokens))
    #if

    ans = []
    begin = 0
    for end in slices:
        ans.append(' '.join(tokens[begin:end]))
        begin = end
    #for

    return ans
#fill


def align(lines: list[str],
          alignArg: str,
          tabWidth: int = 4,
          collapseSpaces: bool = False
          ) -> list:
    """
    Aligns lines left, right or centre wrt the length of the longest line.

    :param lines:          list of input lines.  If empty, returns [].

    :param alignArg:       alignment option: 'l' (left), 'r' (right) or
                           'c' (centre).

    :param tabWidth:       if not 0, replaces tabs by this many spaces.
                           Has no effect if 'collapseSpaces' is True.

    :param collapseSpaces: if true, replaces all space clusters by single
                           spaces, or double spaces if they follow a period.

    :returns: List of aligned non-newline-terminated lines.

    :raises: ValueError
    """
    if tabWidth < 0:
        raise ValueError("'tabWidth' must be >= 0")
    #if

    if not lines:
        return []
    #if

    if collapseSpaces:
        f = lambda s : re.sub("\\. ", ".  ",
                              re.sub("[ \t\f\v\r\n]+", ' ', s.strip(_BLANKS), count=0),
                              count=0)
    elif tabWidth:
        tab = tabWidth * ' '
        f = lambda s : s.strip(_BLANKS).replace('\t', tab)
    else:
        f = lambda s : s.strip(_BLANKS)
    #else

    maxLength = 0
    for i in range(len(lines)):
        lines[i] = f(lines[i])
        maxLength = max(maxLength, len(lines[i]))
    #for

    if alignArg == 'l':
        f = lambda line : line.ljust(maxLength)
    elif alignArg == 'r':
        f = lambda line : line.rjust(maxLength)
    elif alignArg == 'c':
        f = lambda line : line.center(maxLength)
    else:
        raise ValueError("'dir' must be 'l', 'r' or 'c'")
    #else

    return [ f(line) for line in lines ]
#align


class Col16:
    """
    16-colour palette composed of two 8-colour groups.
    The colours in the second group are the same as the ones
    in the first group, but brighter.  To choose a colour from the brighter
    group, add Col16.BRIGHT, e.g. Col16.YELLOW + Col16.BRIGHT.

    Base colours:
        - Col16.BLACK
        - Col16.RED
        - Col16.GREEN
        - Col16.YELLOW
        - Col16.BLUE
        - Col16.PURPLE
        - Col16.CYAN
        - Col16.WHITE
    """
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37
    BRIGHT = 60
#Colours


class Palette:
    """
    IDs for colour palettes:
        - Palette.GREYSCALE
        - Palette.COL16
        - Palette.COL256
    """
    GREYSCALE, COL16, COL256 = range(3)
#Palette


def colourise(s: str,
              foreground: int = None,
              background: int = None,
              inverted: bool = False,
              palette: int = Palette.COL16,
              bold: bool = False,
              italics: bool = False,
              underline: bool = False,
              strikethrough: bool = False,
              blinking: bool = False
              ) -> str:
    """
    Returns a copy of the input string 's', but with ANSI escape codes that will
    make the text and its background have the chosen colours and characteristics
    when printed on the terminal.

    :param s:             the input string

    :param foreground:    the foreground colour.  If None, leaves the foreground
                          colour unspecified so the console will use the default
                          colour.

    :param background:    the background colour.  If None, leaves the background
                          colour unspecified so the console will use the default
                          colour.

    :param inverted:      if True, foreground and background colours are
                          exchanged.

    :param palette:       Palette.GREYSCALE, Palette.COL16 or Palette.COL256.
                          This determines how 'foreground' and 'background'
                          are interpreted.

    :param bold:          if True, the text font is bold.

    :param italics:       if True, the text font is slanted.

    :param underline:     if True, the text is underlined.

    :param strikethrough: if True, the text is struck-through.

    :param blinking:      if True, the text blinks.

    If 'palette' is Palette.COL16, 'foreground' and 'background' may be one
    of the colours defined in Class Col16, optionally with the bright
    switch.  For example:

    ::

        colourise(s,
                  foreground = Colours.RED,
                  background = Colours.YELLOW + Colours.BRIGHT
                  )

    If 'palette' is Palette.GREYSCALE, 'foreground' and 'background' must be
    integers between 0 and 24, where 0 is black and 24 is white.

    If 'palette' is Palette.COL256, 'foreground' and 'background' must be
    integers between 0 and 255.  Use getPalette(...) to see what colour each
    number produces.

    :raises: ValueError if 'palette' has a wrong value.  The 'foreground' and
             'background' values are not checked.  Wrong 'foreground' and
             'background' values are not critical.  They will simply produce the
             wrong colour (or none at all).
    """
    tokens = []

    if palette == Palette.COL16:
        if foreground is not None:
            tokens.append(str(foreground))
        #if
        if background is not None:
            tokens.append(str(background + 10))
        #if

    elif palette == Palette.COL256:
        if foreground is not None:
            tokens.extend([ '38', '5', str(foreground) ])
        #if
        if background is not None:
            tokens.extend([ '48', '5', str(background) ])
        #if

    elif palette == Palette.GREYSCALE:
        colour = lambda n : 231 if n == 24 else n + 232

        if foreground is not None:
            tokens.extend([ '38', '5', str(colour(foreground)) ])
        #if
        if background is not None:
            tokens.extend([ '48', '5', str(colour(background)) ])
        #if

    else:
        raise ValueError("'palette' must be Palette.GREYSCALE, "
                         "Palette.COL16 or Palette.COL256")
    #else

    if bold:
        tokens.append('1')
    #if
    if italics:
        tokens.append('3')
    #if
    if underline:
        tokens.append('4')
    #if
    if blinking:
        tokens.append('5')
    #if
    if inverted:
        tokens.append('7')
    #if
    if strikethrough:
        tokens.append('9')
    #if

    return "\033[%sm%s\033[m" % (';'.join(tokens), s)
#colourise


def getPalette(palette: int) -> str:
    """
    Returns a string that shows all colours of the chosen palette.

    :param palette: Palette.GREYSCALE, Palette.COL16 or Palette.COL256.

    :raises: ValueError
    """

    if palette == Palette.COL16:
        colouriseF = lambda _s, _c : colourise(_s, foreground=_c, palette=palette)
        colouriseB = lambda _s, _c : colourise(_s, background=_c, palette=palette)

        s = lambda _n, _c : colouriseF(_n.rjust(10), _c) \
                            + colouriseF(_n.rjust(10), _c + Col16.BRIGHT) \
                            + "  " + colouriseB(_n.rjust(8), _c) \
                            + "  " + colouriseB(_n.rjust(8), _c + Col16.BRIGHT)

        return '\n'.join([s("black", Col16.BLACK),
                          s("red", Col16.RED),
                          s("green", Col16.GREEN),
                          s("yellow", Col16.YELLOW),
                          s("blue", Col16.BLUE),
                          s("purple", Col16.PURPLE),
                          s("cyan", Col16.CYAN),
                          s("white", Col16.WHITE),
                          ])

    elif palette == Palette.COL256:
        n = lambda _n1, _n2 : _n1 * 8 + _n2
        strn = lambda _n1, _n2 : str(n(_n1, _n2)).rjust(4).ljust(5)

        s = lambda _n1, _n2 : colourise(strn(_n1, _n2),
                                        foreground=n(_n1, _n2),
                                        palette=palette
                                        )
        p = lambda : '\n'.join([ ''.join([ s(n1, n2) for n2 in range(8) ])
                                 for n1 in range(32) ])

        palette1 = p()

        s = lambda _n1, _n2 : colourise(strn(_n1, _n2),
                                        background=n(_n1, _n2),
                                        palette=palette
                                        )
        palette2 = p()

        return "%s\n\n%s" % (palette1, palette2)

    elif palette == Palette.GREYSCALE:
        colouriseF = lambda _n : colourise(str(_n).rjust(3).ljust(4),
                                          foreground=_n,
                                          palette=palette)
        colouriseB = lambda _n : colourise(str(_n).rjust(3).ljust(4),
                                          background=_n,
                                          palette=palette)
        s = lambda _n : colouriseF(_n) + colouriseB(_n)

        return '\n'.join([ s(i) for i in range(25) ])

    else:
        raise ValueError("'palette' must be Palette.GREYSCALE, "
                         "Palette.COL16 or Palette.COL256")
    #else
#getPalette


### aczutro ###################################################################
