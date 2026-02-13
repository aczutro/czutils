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
Command-line application to format text in a variety of ways.
"""
from .textformat import CommandLineParser

from ..lib import czoutline, cztext

import io
import logging
import sys


def textFormat(text: str, action: str,
               align: str = 'l',
               lineWidth: int = 70,
               lvlWidth: int = 1,
               processComments: bool = False,
               printComments: bool = True,
               boldHeadings: bool = True
               ) -> str:
    """
    Reformats given text and returns it as a string.

    :param text:               input text.

    :param action:             'a', 'f' or 'o'
                               If 'a', only aligns lines, preserving original
                               line breaks.
                               If 'f', fills lines, preserving paragraph
                               breaks, and aligns them.
                               If 'o', interprets input text as
                               czoutline.Outliner markup and formats it
                               accordingly.

    :param align:              'l' (left), 'r' (right) or 'c' (right).
                               Ignored if 'action' is 'o'.

    :param lineWidth:          Maximum line width.  Must be > 9.
                               Ignored if 'action' is 'a'.

    :param lvlWidth:           Number of spaces per indentation level. Must be
                               >= 0.  Ignored if 'action' is not 'o'.

    :param processComments:    If True, lines starting with '#' are regarded as
                               comments.  Ignored if 'action' is not 'o'.

    :param printComments:      If True, comments are included in the output (as
                               comments).  Ignored if 'action' is not 'o'.

    :param boldHeadings:       If True, uses bold styles for headings.
                               Ignored if 'action' is not 'o'.

    :returns: a single string containing the formatted text

    :raises: ValueError
    """
    if action == 'a':
        lines = text.splitlines()
        return '\n'.join(cztext.align(lines, align, collapseSpaces=True))

    elif action == 'f':
        ans = []
        for par in cztext.paragraphy(text):
            ans.extend(cztext.fill(par, lineWidth=lineWidth))
            ans.append("")
        #for
        if ans and ans[-1] == "":
            ans.pop(-1)
        #if
        return '\n'.join(cztext.align(ans, align,
                                      tabWidth=0,  # fill already handled tabs
                                      collapseSpaces=False  # wrap already handled space clusters
                                      ))
    elif action == 'o':
        ans = io.StringIO()
        OL = czoutline.Outliner(stream=ans,
                                lineWidth=lineWidth,
                                lvlWidth=lvlWidth,
                                processComments=processComments,
                                printComments=printComments,
                                h1Style=czoutline.Style.BOLD_YELLING if boldHeadings \
                                    else czoutline.Style.YELLING,
                                h2Style=czoutline.Style.BOLD_TITLE if boldHeadings \
                                    else czoutline.Style.TITLE,
                                h3Style=czoutline.Style.BOLD_TITLE if boldHeadings \
                                    else czoutline.Style.TITLE,
                                bulletStyle=czoutline.Style.BOLD if boldHeadings \
                                    else czoutline.Style.NORMAL
                                )
        OL << text
        return ans.getvalue()

    else:
        raise ValueError("'args.action' must be 'f' or 'p'")
    #else

#textFormat


def main():
    """
    Main routine for command-line app 'textformat'.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.CRITICAL)

    CLP = CommandLineParser()
    args = CLP.parseCommandLine()
    logger.info(args)
    text = sys.stdin.read()
    ifExists = lambda _key : vars(args)[_key] if _key in vars(args) else None
    print(textFormat(text, args.action,
                     align=ifExists('align'),
                     lineWidth=ifExists('lineWidth'),
                     lvlWidth=ifExists('lvlWidth'),
                     processComments=ifExists('processComments'),
                     printComments=ifExists('printComments'),
                     boldHeadings=ifExists('boldHeadings')
                     ))
    sys.exit(0)
#main


if __name__ == '__main__':
    main()
#if


### aczutro ###################################################################
