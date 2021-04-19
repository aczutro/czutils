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
Text aligner and reformatter.
"""

from nacl.exceptions import ValueError

from ..private.fill import Args, CommandLineParser

from ..utils import czlogging
from ..utils import czsystem

import sys
import re
import textwrap


def paragraphy(text, fixSentenceEndings: bool = True) -> list:
    """
    Splits text into paragraphs.  Detects paragraph breaks by searching for
    empty lines.  (An empty line has the form "\n[ \t]*\n".)

    Does not produce empty paragraphs.  I.e., e.g., that "a\n\n\n\nb" becomes
    ["a", "b"].

    :param text:               Can be a single string or a list of strings.
                               If the latter, paragraphy assumes that no string
                               in the list contains '\n' characters.
    :param fixSentenceEndings: If true, makes sure that periods that end a
                               sentence are followed by 2 spaces, unless it's
                               the paragraphs last sentence.

    :returns: A list of strings where each string is a paragraph.

    :raises: TypeError
    """
    if not text:
        return []
    #if

    blanks = ' \t\n'

    if isinstance(text, str):
        return paragraphy(text.strip(blanks).splitlines(), fixSentenceEndings)

    elif isinstance(text, list):
        breaks = []
        N = len(text)
        begin = 0
        for i in range(N):
            text[i] = text[i].strip(blanks)
            if not text[i]:
                breaks.append((begin, i))
                begin = i + 1
            #if
        #for
        breaks.append((begin, N))

        if fixSentenceEndings:
            f = lambda s : re.sub("\\.[ \t]+", ".  ", s, count=0)
        else:
            f = lambda s : s
        #else

        ans = []
        for begin, end in breaks:
            if begin != end:
                ans.append(f(' '.join(text[begin:end])))
            #if
        #for

        return ans

    else:
        raise TypeError("'text' must be str or list of str")
    #else

#paragraphy


def wrap(text: str,
         lineWidth : int = 70,
         fixSentenceEndings: bool = False,
         tabWidth: int = 1) -> list:
    """
    Reformats a given text so that all lines are as full as possible but not
    longer than 'lineWidth' characters.  Preserves the text's paragraph breaks.

    :param text:               input text.
    :param lineWidth:          maximum line length.  Must be > 9.
    :param fixSentenceEndings: If true, makes sure that periods that end a
                               sentence are followed by 2 spaces, unless it's
                               the paragraphs last sentence.
    :param tabWidth:           If not 0, replace tabs by this many spaces.


    :return: A list of strings, where each string is a non-'\n'-terminated line.

    :raises: ValueError
    """
    if lineWidth < 10:
        raise ValueError("'lineWidth' must be > 9")
    #if
    if tabWidth < 0:
        raise ValueError("'tabWidth' must be >= 0")
    #if

    paragraphs = paragraphy(text, fixSentenceEndings=fixSentenceEndings)

    if not paragraphs:
        return []
    #if

    expandTabs = tabWidth != 0

    tw = textwrap.TextWrapper(width=lineWidth,
                              fix_sentence_endings=fixSentenceEndings,
                              break_long_words=False,
                              expand_tabs=expandTabs,
                              tabsize=tabWidth
                              )
    ans = []
    for par in paragraphs:
        ans.extend(tw.wrap(par))
        ans.append("")
    #for
    ans.pop(-1)

    return ans
#wrap


def align(lines: list, dir: str,
          tabWidth: int = 4,
          fixSentenceEndings: bool = False) -> list:
    """
    Aligns lines left, right or centre wrt the length of the longest line.

    :param lines:              list of input lines.  If empty, returns [].
    :param dir:                alignment direction: 'l' (left), 'r' (right) or
                               'c' (centre).
    :param tabWidth:           if not 0, replaces tabs by this many spaces.
    :param fixSentenceEndings: If true, makes sure that periods that end a
                               sentence are followed by 2 spaces, unless it's
                               the paragraphs last sentence.

    :returns: List of aligned non-'\n'-terminated lines.

    :raises: ValueError
    """
    if not lines:
        return []
    #if
    if tabWidth < 0:
        raise ValueError("'tabWidth' must be >= 0")
    #if

    blanks = ' \t\n'
    tab = tabWidth * ' '

    if tabWidth and fixSentenceEndings:
        f = lambda s : re.sub("\\.[ \t]+",
                              ".  ",
                              s.strip(blanks).replace('\t', tab),
                              count=0)
    elif tabWidth and not fixSentenceEndings:
        f = lambda s : s.strip(blanks).replace('\t', tab)
    elif fixSentenceEndings:
        f = lambda s : re.sub("\\.[ \t]+",
                              ".  ",
                              s.strip(blanks),
                              count=0)
    else:
        f = lambda s : s.strip(blanks)
    #else

    maxLength = 0
    for i in range(len(lines)):
        lines[i] = f(lines[i])
        maxLength = max(maxLength, len(lines[i]))
    #for

    if dir == 'l':
        f = lambda line : line.ljust(maxLength)
    elif dir == 'r':
        f = lambda line : line.rjust(maxLength)
    elif dir == 'c':
        f = lambda line : line.center(maxLength)
    else:
        raise ValueError("'dir' must be 'l', 'r' or 'c'")
    #else

    for i in range(len(lines)):
        lines[i] = f(lines[i])
    #for

    return lines
#align


def fill(text: str, args: Args) -> list:
    """
    Reformats given text and returns it as a list of non-'\n'-terminated lines.

    The attributes of 'args' are interpreted as follows:

      - args.action:             'p' or 'f'.
                                 If 'p', preserves original line breaks.
                                 If 'f', wraps lines so that all lines are as
                                 full as possible but not longer than
                                 option.lineWidth characters.
                                 Preserves paragraph breaks.
      - args.align:              'l', 'r' or 'c'.
                                 Aligns all lines left, right or centre, resp.
      - args.lineWidth:          Line width for fill option.  Must be > 9.
      - args.tabWidth:           If not 0, replaces tabs by this many spaces.
      - args.fixSentenceEndings: If true, makes sure that periods that end a
                                 sentence are followed by 2 spaces, unless it's
                                 the paragraphs last sentence.

    :param text: input text.
    :param args: data collection with all necessary input arguments.

    :returns: list of strings.  Each string corresponds to a line.

    :raises: ValueError
    """
    if args.action == 'f':
        lines = wrap(text,
                     lineWidth=args.lineWidth,
                     fixSentenceEndings=args.fixSentenceEndings,
                     tabWidth=args.tabWidth)
        return align(lines, args.align,
                     tabWidth=0,  # wrap already handled tabs
                     fixSentenceEndings=False  # wrap already handled sentence endings
                     )
    elif args.action == 'p':
        lines = text.splitlines()
        return align(lines, args.align,
                     tabWidth=args.tabWidth,
                     fixSentenceEndings=args.fixSentenceEndings
                     )
    else:
        raise ValueError("'args.action' must be 'f' or 'p'")
    #else
#fill


def main():
    """
    Main routine for command-line app fill.
    """
    L = czlogging.LogChannel(czsystem.appName())
    try:
        CLP = CommandLineParser()
        options = CLP.parseCommandLine(10)
        L.info(options)
        text = sys.stdin.read()
        lines = fill(text, options)
        print('\n'.join(lines))
        sys.exit(0)
    except AssertionError as e:
        raise e
    except Exception as e:
        L.error(e)
        sys.exit(2)
    #except
#main


### aczutro ###################################################################
