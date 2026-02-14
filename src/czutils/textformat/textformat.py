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

from .clp import Args
from ..lib import czoutline, cztext

import io


def textFormat(text: str, args: Args) -> str:
    """
    Reformats given text and returns it as a string.

    :param text: input text.


    :param args: Contains the following attributes:

                 action:          'a', 'f' or 'o'
                                  If 'a', only aligns lines, preserving original
                                  line breaks.
                                  If 'f', fills lines, preserving paragraph
                                  breaks, and aligns them.
                                  If 'o', interprets input text as
                                  czoutline.Outliner markup and formats it
                                  accordingly.

                 align:           'l' (left), 'r' (right) or 'c' (right).
                                  Ignored if 'action' is 'o'.

                 lineWidth:       Maximum line width.  Must be > 9.
                                  Ignored if 'action' is 'a'.

                 lvlWidth:        Number of spaces per indentation level. Must be
                                  >= 0.  Ignored if 'action' is not 'o'.

                 processComments: If True, lines starting with '#' are regarded as
                                  comments.  Ignored if 'action' is not 'o'.

                 printComments:   If True, comments are included in the output (as
                                  comments).  Ignored if 'action' is not 'o'.

                 boldHeadings:    If True, uses bold styles for headings.
                                  Ignored if 'action' is not 'o'.

    :returns: a single string containing the formatted text

    :raises: ValueError
    """
    if args.action == 'a':
        lines = text.splitlines()
        return '\n'.join(cztext.align(lines, args.align, collapseSpaces=True))

    elif args.action == 'f':
        ans = []
        for par in cztext.paragraphy(text):
            ans.extend(cztext.fill(par, lineWidth=args.lineWidth))
            ans.append("")
        #for
        if ans and ans[-1] == "":
            ans.pop(-1)
        #if
        return '\n'.join(cztext.align(ans, args.align,
                                      tabWidth=0,  # fill already handled tabs
                                      collapseSpaces=False  # wrap already handled space clusters
                                      ))
    elif args.action == 'o':
        ans = io.StringIO()
        OL = czoutline.Outliner(stream=ans,
                                lineWidth=args.lineWidth,
                                lvlWidth=args.lvlWidth,
                                processComments=args.processComments,
                                printComments=args.printComments,
                                h1Style=(czoutline.Style.BOLD_YELLING
                                         if args.boldHeadings
                                         else czoutline.Style.YELLING
                                         ),
                                h2Style=(czoutline.Style.BOLD_TITLE
                                         if args.boldHeadings
                                         else czoutline.Style.TITLE
                                         ),
                                h3Style=(czoutline.Style.BOLD_TITLE
                                         if args.boldHeadings
                                         else czoutline.Style.TITLE
                                         ),
                                bulletStyle=(czoutline.Style.BOLD
                                             if args.boldHeadings
                                             else czoutline.Style.NORMAL
                                             ),
                                )
        OL << text
        return ans.getvalue()

    else:
        raise ValueError("'args.action' must be 'f' or 'p'")
    #else

#textFormat


### aczutro ###################################################################
