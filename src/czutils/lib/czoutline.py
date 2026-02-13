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
A document formatter for text displayed on a purely text-based medium, like the
command line terminal or the text editor.
"""
from ..lib import czmath, cztext

import re
import sys
from typing import Callable, TextIO


class Style:
    """
    Defines a set of predefined string styles for Outliner.

    Styles are functions (lambdas) that map a 1-line string
    to another 1-line string (for example, applying colourisation),
    or an integer to a 1-line string.

    str -> str, for heading and bullet styles:

    - YELLING: all-caps text
    - TITLE:   each word is capitalised
    - NORMAL:  text is unchanged

    - BOLD_YELLING: like YELLING, but font weight is bold
    - BOLD_TITLE:   like TITLE, but font weight is bold
    - BOLD:         like NORMAL, but font weight is bold

    int -> str, for list number styles:

    - ARABIC_DOT:     e.g. 1 -> "1."
    - ARABIC_COLON:   e.g. 1 -> "1:"
    - ARABIC_BRACKET: e.g. 1 -> "1)"
    - ARABIC_SQUARE:  e.g. 1 -> "[1]"

    - ALPHA_DOT:     e.g. 1 -> "a."
    - ALPHA_COLON:   e.g. 1 -> "a:"
    - ALPHA_BRACKET: e.g. 1 -> "a)"
    - ALPHA_SQUARE:  e.g. 1 -> "[a]"

    - ROMAN_DOT:     e.g. 1 -> "i."
    - ROMAN_COLON:   e.g. 1 -> "i:"
    - ROMAN_BRACKET: e.g. 1 -> "i)"
    - ROMAN_SQUARE:  e.g. 1 -> "[i]"

    - CAP_ROMAN_DOT:     e.g. 1 -> "I."
    - CAP_ROMAN_COLON:   e.g. 1 -> "I:"
    - CAP_ROMAN_BRACKET: e.g. 1 -> "I)"
    - CAP_ROMAN_SQUARE:  e.g. 1 -> "[I]"
    """
    YELLING = lambda s : s.upper()
    TITLE = lambda s : s.title()
    NORMAL = lambda s : s

    BOLD_YELLING = lambda s : cztext.colourise(s.upper(), bold=True)
    BOLD_TITLE = lambda s : cztext.colourise(s.title(), bold=True)
    BOLD = lambda s : cztext.colourise(s, bold=True)

    ARABIC_DOT = lambda i : "%d." % i
    ARABIC_COLON = lambda i : "%d:" % i
    ARABIC_BRACKET = lambda i : "%d)" % i
    ARABIC_SQUARE = lambda i : "[%d]" % i

    ALPHA_DOT = lambda i : "%s." % chr(96 + i)
    ALPHA_COLON = lambda i : "%s:" % chr(96 + i)
    ALPHA_BRACKET = lambda i : "%s)" % chr(96 + i)
    ALPHA_SQUARE = lambda i : "[%s]" % chr(96 + i)

    ROMAN_DOT = lambda i : "%s." % czmath.arabic2roman(i).lower()
    ROMAN_COLON = lambda i : "%s:" % czmath.arabic2roman(i).lower()
    ROMAN_BRACKET = lambda i : "%s)" % czmath.arabic2roman(i).lower()
    ROMAN_SQUARE = lambda i : "[%s]" % czmath.arabic2roman(i).lower()

    CAP_ROMAN_DOT = lambda i : "%s." % czmath.arabic2roman(i)
    CAP_ROMAN_COLON = lambda i : "%s:" % czmath.arabic2roman(i)
    CAP_ROMAN_BRACKET = lambda i : "%s)" % czmath.arabic2roman(i)
    CAP_ROMAN_SQUARE = lambda i : "[%s]" % czmath.arabic2roman(i)
#Style


class Outliner:
    """
    Provides a document
    formatter for text displayed on a purely text-based medium, like
    the command line terminal or the text editor.

    The premise is that the text-based environment does not provide
    different font styles or colours.  Hence, structure is achieved
    solely through indentation.

    Currently supported items are level-1, level-2 and level-3 headings,
    paragraphs and verbatim sections.  Indenting is handled automatically
    depending in heading levels, but the indentation level can also be manually
    increased or decreased.
    """

    def __init__(self,
                 stream: TextIO = sys.stdout,
                 processComments: bool = True,
                 printComments: bool = False,
                 lineWidth: int = 70,
                 lvlWidth: int = 4,
                 spacedLItems : bool = False,
                 spacedDItems : bool = True,
                 maxFirstIndex: int = 9,
                 h1Style: Callable[[str], str] = Style.BOLD_YELLING,
                 h2Style: Callable[[str], str] = Style.BOLD_TITLE,
                 h3Style: Callable[[str], str] = Style.BOLD_TITLE,
                 bulletStyle: Callable[[str], str] = Style.BOLD,
                 numberStyle: Callable[[str], str] = Style.ARABIC_DOT,
                 keyStyle: Callable[[str], str] = Style.BOLD
                 ):
        """

        :param stream:          The stream to write to.  Can be a file, a system
                                stream or a string stream.

        :param processComments: If True, lines starting with '#' are regarded as
                                comments.  Otherwise, they are processed like
                                normal text.

        :param printComments:   If True, comments are printed (as comments).
                                If False, they are suppressed.
                                Has no effect if 'processComments' is False.

        :param lineWidth:       Maximum line width for paragraphs.

        :param lvlWidth:        Number of spaces per indentation level.

        :param spacedLItems:    If True, an empty line is printed between items
                                of ordered and unordered lists.

        :param spacedDItems:    If True, an empty line is printed between
                                items of dictionary lists.

        :param maxFirstIndex:   Maximum number that the parser will accept as a
                                numbered list item command.  Must be >= 0.
                                Note that the parser's performance will suffer
                                if this number is too high.

        :param h1Style:         Style for level-1 headers.  May be a predefined
                                style from Class Style, or any lambda that takes
                                a string and returns a string.

        :param h2Style:         Style for level-2 headers.  May be a predefined
                                style from Class Style, or any lambda that takes
                                a string and returns a string.

        :param h3Style:         Style for level-3 headers.  May be a predefined
                                style from Class Style, or any lambda that takes
                                a string and returns a string.

        :param bulletStyle:     Style for list bullets.  May be a predefined
                                style from Class Style, or any lambda that takes
                                a string and returns a string.

        :param numberStyle:     Style for numbers in ordered lists.  Must be a
                                lambda that takes an integer and returns a
                                string.  The bullet style (typically
                                colourisation) is applied on top of it.

        :param keyStyle:        Style for dictionary list keys.  May be a
                                predefined style from Class Style, or any lambda
                                that takes a string and returns a string.
        """
        self._print = lambda *args : print(*args, file=stream)

        self._processComments = processComments
        self._printComments = printComments

        self._fH1 = h1Style
        self._fH2 = h2Style
        self._fH3 = h3Style
        self._fBullet = bulletStyle
        self._fNumber = numberStyle
        self._fKey = keyStyle

        self._lineWidth = lineWidth
        self._lvlWidth = lvlWidth
        self._maxLevel = self._lineWidth // self._lvlWidth

        self._spacedLItems = spacedLItems
        self._spacedDItems = spacedDItems
        self._bullet = -1
        self._numberPrefixes = tuple("%d. " % i for i in range(maxFirstIndex + 1)) \
                               + tuple("%d.\t" % i for i in range(maxFirstIndex + 1))

        self._level = -1
        self._indent = ""
        self._setLevel(0)
    #__init__


    def setH1Style(self, style: Callable[[str], str]):
        """
        Sets style for level-1 headers.

        :param style: May be a predefined style from Class Style, or any lambda
                      that takes a string and returns a string.
        """
        self._fH1 = style
    #setH1Style


    def setH2Style(self, style: Callable[[str], str]):
        """
        Sets style for level-2 headers.

        :param style: May be a predefined style from Class Style, or any lambda
                      that takes a string and returns a string.
        """
        self._fH2 = style
    #setH2Style


    def setH3Style(self, style: Callable[[str], str]):
        """
        Sets style for level-3 headers.

        :param style: May be a predefined style from Class Style, or any lambda
                      that takes a string and returns a string.
        """
        self._fH3 = style
    #setH3Style


    def setLineWidth(self, lineWidth: int):
        """
        Sets maximum line width for paragraphs.

        :param lineWidth: An integer, preferably positive.
        """
        self._lineWidth = lineWidth
        self._maxLevel = self._lineWidth // self._lvlWidth
        self._setLevel(self._level)
    #setLineWidth


    def setLvlWidth(self, lvlWidth: int):
        """
        Sets number of spaces to indent per indentation level.

        :param lvlWidth: An integer, preferably positive.
        """
        self._lvlWidth = lvlWidth
        self._maxLevel = self._lineWidth // self._lvlWidth
        self._setLevel(self._level)
    #setLvlWidth


    def h1(self, line: str):
        """
        Prints a level-1 header.

        :param line: A string representing a single line.  All blank clusters
                     (include newlines) are replaced by single spaces, and the
                     line is wrapped if it is too long.
        """
        self._h(line, 0, self._fH1)
    #h1


    def h2(self, line: str):
        """
        Prints a level-2 header.

        :param line: A string representing a single line.  All blank clusters
                     (include newlines) are replaced by single spaces, and the
                     line is wrapped if it is too long.
        """
        self._h(line, 1, self._fH2)
    #h2


    def h3(self, line: str):
        """
        Prints a level-3 header.

        :param line: A string representing a single line.  All blank clusters
                     (include newlines) are replaced by single spaces, and the
                     line is wrapped if it is too long.
        """
        self._h(line, 2, self._fH3)
    #h3


    def _h(self, line: str, level: int, fStyle: Callable[[str], str]):
        """
        Prints a level-n header.

        :param line:   A string representing a single line.  Newline characters
                       are converted into spaces.

        :param level:  An integer, preferably positive

        :param fStyle: a lambda that takes a string and returns a string.
        """
        self._setLevel(level)
        self._print("")
        for _line in cztext.fill(line,
                                 lineWidth=self._lineWidth - len(self._indent)):
            if _line:
                self._print(self._indent + fStyle(_line))
            #if
        #for
        self._setLevel(level + 1)
    #_h


    def inc(self):
        """
        Increments the indentation level by 1.
        """
        self._setLevel(self._level + 1)
    #inc


    def dec(self):
        """
        Decrements the indentation level by 1.
        """
        self._setLevel(0 if self._level == 0 else self._level - 1)
    #dec


    def _setLevel(self, level: int):
        """
        Sets the indentation level (and the indent string).
        """
        self._level = level if level < self._maxLevel else self._maxLevel - 1
        self._indent = self._level * self._lvlWidth * ' '
    #_setLevel


    def verbatim(self, text):
        """
        Prints a verbatim section without any formatting, keeping all the
        original line breaks.  However, the section is indented to match the
        document's indentation level.

        :param text: May be a single string or a list of strings.  If the
                     latter, 'verbatim' assumes that each string in the list is
                     a line containing no newline characters.
        """
        if isinstance(text, str):
            self.verbatim(text.splitlines())
        elif isinstance(text, list):
            self._print("")
            self._print('\n'.join([ self._indent + line for line in text ]))
        else:
            raise ValueError("'text' must be a string or a list of strings")
        #else
    #verbatim


    def ul(self,
           spacedLItems: bool = None,
           bulletStyle: Callable[[str], str] = None
           ):
        """
        Starts an unordered (bulleted) list.

        :param spacedLItems: If True, an empty line is printed between items.
                             If None, reuses the last setting.

        :param bulletStyle:  Style for list bullets.  May be a predefined style
                             from Class Style, or any lambda that takes a string
                             and returns a string.
                             If None, reuses the last setting.
        """
        self._bullet = -1
        if spacedLItems is not None:
            self._spacedLItems = spacedLItems
        #if
        if not self._spacedLItems:
            self._print("")
        #if
        if bulletStyle is not None:
            self._fBullet = bulletStyle
        #if
    #ul


    def ol(self,
           n : int = 1,
           spacedLItems: bool = None,
           bulletStyle: Callable[[str], str] = None,
           numberStyle: Callable[[str], str] = None
           ):
        """
        Starts an ordered (numbered) list.

        :param n:            Index for the first item.  If less than 0,
                             the list becomes unordered (bulleted).

        :param spacedLItems: If True, an empty line is printed between items.
                             If None, reuses the last setting.

        :param bulletStyle:  Style for list bullets.  May be a predefined style
                             from Class Style, or any lambda that takes a string
                             and returns a string.
                             If None, reuses the last setting.

        :param numberStyle:  Style for numbers in ordered lists.  Must be a
                             lambda that takes an integer and returns a string.
                             The bullet style (typically colourisation) is
                             applied on top of it.
                             If None, reuses the last setting.
        """
        self._bullet = n
        if spacedLItems is not None:
            self._spacedLItems = spacedLItems
        #if
        if not self._spacedLItems:
            self._print("")
        #if
        if bulletStyle is not None:
            self._fBullet = bulletStyle
        #if
        if numberStyle is not None:
            self._fNumber = numberStyle
        #if
    #ol


    def dl(self,
           spacedDItems: bool = None,
           keyStyle: Callable[[str], str] = None
           ):
        """
        Starts a dictionary list, i.e. a list where each list item
        is composed of a key and a description of the key.  For example:

        ::

            hat   A covering for the head that is not part of a piece of
                  clothing.
            shoe  A covering for the foot, usually made of a strong material
                  such as leather, with a thick leather or plastic sole and a
                  heel.
            trousers
                  A piece of clothing that covers the lower part of the body
                  from the waist to the feet.

        :param spacedDItems: If True, an empty line is printed between items.
                             If None, reuses the last setting.
        :param keyStyle:     Style for item keys.  May be a predefined style
                             from Class Style, or any lambda that takes a string
                             and returns a string.
                             If None, reuses the last setting.
        """
        if spacedDItems is not None:
            self._spacedDItems = spacedDItems
        #if
        if not self._spacedDItems:
            self._print("")
        #if
        if keyStyle is not None:
            self._fKey = keyStyle
        #if
    #list


    def li(self, text: str):
        """
        Prints a list item.   ol or ul must be called first.

        :param text: A string representing a single paragraph.
        """
        paragraph = cztext.fill(text,
                                lineWidth=self._lineWidth
                                          - len(self._indent)
                                          - self._lvlWidth * 2
                                )
        if paragraph:
            firstLineIndent = self._indent + self._lvlWidth * ' '
            otherLineIndent = self._indent + self._lvlWidth * 2 * ' '
            if self._spacedLItems:
                self._print("")
            #if
            if self._bullet < 0:
                bullet = self._fBullet('-') + (self._lvlWidth - 1) * ' '
            else:
                number = self._fNumber(self._bullet)
                bullet = self._fBullet(number) + (self._lvlWidth - len(number)) * ' '
                self._bullet += 1
            #else
            self._print(firstLineIndent + bullet + paragraph[0])
            for line in paragraph[1:]:
                self._print(otherLineIndent + line)
            #for

        #if
    #li

    def di(self, key: str, description: str):
        """
        Prints a dictionary list item.   dl must be called first.

        :param key:         A preferably short string.
        :param description: A string representing a single paragraph.
        """
        keyPar = cztext.fill(key,
                             lineWidth=self._lineWidth - len(self._indent)
                             )
        textPar = cztext.fill(description,
                              lineWidth=self._lineWidth
                                        - len(self._indent)
                                        - self._lvlWidth * 2
                              )
        if len(keyPar) * len(textPar) == 0:
            return
        #if
        if self._spacedDItems:
            self._print("")
        #if
        indentDiff = 2 * self._lvlWidth
        firstLineIndent = self._indent
        otherLineIndent = self._indent + indentDiff * ' '
        for line in keyPar[:-1]:
            self._print(firstLineIndent + self._fKey(line))
        #for
        if len(keyPar[-1]) < indentDiff:
            self._print(firstLineIndent + self._fKey(keyPar[-1])
                        + (indentDiff - len(keyPar[-1])) * ' ' + textPar[0]
                        )
        else:
            self._print(firstLineIndent + self._fKey(keyPar[-1]))
            self._print(otherLineIndent + textPar[0])
        #else
        for line in textPar[1:]:
            self._print(otherLineIndent + line)
        #for

    #di


    def __lshift__(self, text: str):
        """
        This function takes a multi-line text and interprets certain patterns
        in it as commands.  Each command corresponds to one of the public
        functions in this class.

        These commands constitute a very simple language which in
        turn is very pretentiously called "Outliner Markup".

        Headings

            Lines starting with asterisks are formatted as headings.

                * level-1 heading
                ** level-2 heading
                *** level-3 heading

        Paragraphs And Indentation

            Lines not starting with 1-3 asterisks are regarded as text
            lines and formatted to fit the maximum line width.  Paragraph
            breaks are marked by empty lines.

            Lines containing only ">>" or "<<" are interpreted as the
            indentation level increment and decrement commands, respectively.
            For example:

                This is a paragraph with indentation level n.
                >>
                This is a new paragraph with indentation level n+1.
                <<
                This is another paragraph with indentation level n.

        Verbatim Sections

            A line containing only "##" starts a verbatim section.
            Another line containing only "##" ends the verbatim section.

        Comments

            Lines starting with '#' are regarded as comments if the
            'processComments' argument was True when this Outliner object was
            initialised.  Otherwise, they are formatted like normal
            text/paragraph lines.

            If regarded as comments, they are printed verbatim (without
            indentation, and with the '#') if the 'printComments' argument
            was True when this Outliner object was initialised.
            Otherwise, they are suppressed from the output.

        :param text: A string.
        """
        h1Prefix = "* "
        h2Prefix = "** "
        h3Prefix = "*** "
        commentPrefix = "#"
        bulletPrefix = ("- ", "+ ", "-\t", "+\t")
        lenBulletPrefix = 2
        dictInfix = "[ \t]::[ \t]"

        indIncCmd = ">>"
        indDecCmd = "<<"
        verbCmd = "##"

        strip = lambda s : s.strip(' \t')

        MODE_PAR, MODE_OL, MODE_UL, MODE_DL = range(4)

        modeLambda = [ lambda p : self._par(p),
                       lambda p : self.li(p),
                       lambda p : self.li(p),
                       lambda p : None
                       ]
        verb = False
        par = []
        previousEmpty = True
        mode = MODE_PAR
        _addPar = lambda m : [ modeLambda[m](par),
                               par.clear(),
                               None ][-1] if par else None

        for line in text.splitlines():
            if strip(line) == verbCmd:
                if verb:
                    verb = False
                else:
                    verb = True
                    self._print("")
                #else
            elif verb:
                self._print(self._indent + line)
            else:
                line = strip(line)
                if not line:
                    _addPar(mode)
                    previousEmpty = True
                elif line == indIncCmd:
                    _addPar(mode)
                    mode = MODE_PAR
                    previousEmpty = False
                    self.inc()
                elif line == indDecCmd:
                    _addPar(mode)
                    mode = MODE_PAR
                    previousEmpty = False
                    self.dec()
                elif line.startswith(h1Prefix):
                    _addPar(mode)
                    mode = MODE_PAR
                    previousEmpty = False
                    self.h1(line[len(h1Prefix):])
                elif line.startswith(h2Prefix):
                    _addPar(mode)
                    mode = MODE_PAR
                    previousEmpty = False
                    self.h2(line[len(h2Prefix):])
                elif line.startswith(h3Prefix):
                    _addPar(mode)
                    mode = MODE_PAR
                    previousEmpty = False
                    self.h3(line[len(h3Prefix):])
                elif line.startswith(bulletPrefix):
                    _addPar(mode)
                    strippedLine = line[lenBulletPrefix:]
                    match = re.search(dictInfix, strippedLine)
                    if match is None:
                        if mode != MODE_UL:
                            mode = MODE_UL
                            self.ul()
                        #if
                        par.append(strippedLine)
                    else:
                        if mode != MODE_DL:
                            mode = MODE_DL
                            self.dl()
                        #if
                        a, b = match.span()
                        modeLambda[MODE_DL] = \
                            lambda p : self.di(strippedLine[:a], p)
                        par.append(strippedLine[b:])
                    #else
                    previousEmpty = False
                elif line.startswith(self._numberPrefixes):
                    _addPar(mode)
                    dotIndex = line.find('.')
                    if mode != MODE_OL:
                        mode = MODE_OL
                        self.ol(n=int(line[:dotIndex]))
                    #if
                    previousEmpty = False
                    par.append(line[dotIndex + 1:])
                elif self._processComments and line.startswith(commentPrefix):
                    if self._printComments:
                        self._print(line)
                    #if
                else:
                    if previousEmpty:
                        mode = MODE_PAR
                    #if
                    previousEmpty = False
                    par.append(line)
                #else
            #else
        #for

        _addPar(mode)
    #put


    def _par(self, text):
        """
        Prints a single paragraph.

        :param text: May be a single string or a list of strings.
        """
        self._print("")
        for line in cztext.fill(text, lineWidth=self._lineWidth - len(self._indent)):
            self._print(self._indent + line)
        #for
    #_par

#Outliner


### aczutro ###################################################################
