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
from ..utils import cztext

import sys
import typing


class Style:
    """
    Defines a set of predefined string styles.  All of them are lambdas that
    take a 1-line string and return a 1-line string.

    - YELLING / BOLD_YELLING: all-caps text
    - TITLE / BOLD_TITLE:     each word is capitalised
    - NORMAL / BOLD:          text is kept unchanged
    """
    YELLING = lambda s : s.upper()
    TITLE = lambda s : s.title()
    NORMAL = lambda s : s

    BOLD_YELLING = lambda s : cztext.colourise(s.upper(), bold=True)
    BOLD_TITLE = lambda s : cztext.colourise(s.title(), bold=True)
    BOLD = lambda s : cztext.colourise(s, bold=True)
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
                 stream: typing.TextIO = sys.stdout,
                 processComments: bool = True,
                 printComments: bool = False,
                 lineWidth: int = 70,
                 lvlWidth: int = 4,
                 h1Style: typing.Callable[[str], str] = Style.BOLD_YELLING,
                 h2Style: typing.Callable[[str], str] = Style.BOLD_TITLE,
                 h3Style: typing.Callable[[str], str] = Style.BOLD_TITLE
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

        :param h1Style:         Style for level-1 headers.  May be a predefined
                                style from Class Style, or any lambda that takes
                                a string and returns a string.

        :param h2Style:         Style for level-2 headers.  May be a predefined
                                style from Class Style, or any lambda that takes
                                a string and returns a string.

        :param h3Style:         Style for level-3 headers.  May be a predefined
                                style from Class Style, or any lambda that takes
                                a string and returns a string.
        """
        self._print = lambda *args : print(*args, file=stream)

        self._processComments = processComments
        self._printComments = printComments

        self._fH1 = h1Style
        self._fH2 = h2Style
        self._fH3 = h3Style

        self._lineWidth = lineWidth
        self._lvlWidth = lvlWidth
        self._maxLevel = self._lineWidth // self._lvlWidth

        self._level = -1
        self._indent = ""
        self._setLevel(0)
    #__init__


    def setH1Style(self, style: typing.Callable[[str], str]):
        """
        Sets style for level-1 headers.

        :param style: May be a predefined style from Class Style, or any lambda
                      that takes a string and returns a string.
        """
        self._fH1 = style
    #setH1Style


    def setH2Style(self, style: typing.Callable[[str], str]):
        """
        Sets style for level-2 headers.

        :param style: May be a predefined style from Class Style, or any lambda
                      that takes a string and returns a string.
        """
        self._fH2 = style
    #setH2Style


    def setH3Style(self, style: typing.Callable[[str], str]):
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
    #h2


    def inc(self):
        """
        Increments the indentation level by 1.
        """
        self._setLevel(self._level + 1)
    #levelInc


    def dec(self):
        """
        Decrements the indentation level by 1.
        """
        self._setLevel(0 if self._level == 0 else self._level - 1)
    #levelInc


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
    #putVerbatim


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
        indIncCmd = ">>"
        indDecCmd = "<<"
        verbCmd = "##"

        strip = lambda s : s.strip(' \t')

        verb = False
        par = []
        _addPar = lambda : [ self._par(par),
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
                    _addPar()
                elif line == indIncCmd:
                    _addPar()
                    self.inc()
                elif line == indDecCmd:
                    _addPar()
                    self.dec()
                elif line.startswith(h1Prefix):
                    _addPar()
                    self.h1(line[len(h1Prefix):])
                elif line.startswith(h2Prefix):
                    _addPar()
                    self.h2(line[len(h2Prefix):])
                elif line.startswith(h3Prefix):
                    _addPar()
                    self.h3(line[len(h3Prefix):])
                elif self._processComments and line.startswith(commentPrefix):
                    if self._printComments:
                        self._print(line)
                    #if
                else:
                    par.append(line)
                #else
            #else
        #for

        _addPar()
    #put


    def _setLevel(self, level: int):
        """
        Sets the indentation level (and the indent string).
        """
        self._level = level if level < self._maxLevel else self._maxLevel - 1
        self._indent = self._level * self._lvlWidth * ' '
    #_setLevel


    def _h(self, line: str, level: int, fStyle: typing.Callable[[str], str]):
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
