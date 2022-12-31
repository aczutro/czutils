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
"Private" help classes and functions used by module app.textformat.
"""
from . import __versionString__

from ..utils import czoutline

import argparse
import os
import sys


def _printOutlineHelp():
    OL = czoutline.Outliner(lineWidth=min(70, os.get_terminal_size().columns))
    OL << """* Outliner markup
    
             Outliner markup is a simple markup language.
               This help text was generated with Outliner
             markup. 
             
             It supports the following elements:
             
             ** headings
             
             Lines starting with asterisks are formatted as headings.  Three
             levels are supported:
             >>  
##
* level-1 heading
** level-2 heading             
*** level-3 heading
##             
             ** paragraphs and indentation

             Lines not starting with 1-3 asterisks are regarded as text lines
             and formatted to fit the maximum line width.  Paragraph breaks are
             marked by empty lines.
               
             Paragraphs are automatically indented to match the 
             indentation level of the heading that precedes them.             
             But the indentation level can also be incremented or decremented
             "manually"
             with a line containing only ">>" or "<<", respectively.
             For example: 
             >>
##
This produces a paragraph with indentation level n.
>> 
This produces a new paragraph with indentation level n+1.
<<
This produces another paragraph with indentation level n.
##             
             <<
             A manually changed indentation level remains valid until the next
             indentation or heading command.
             
             ** verbatim sections
             
             A line containing only "##" starts a verbatim section.  All lines
             in a verbatim section are printed without any formatting, but they
             are indented to match the document's indentation level.  Another
             line containing only "##" ends the verbatim section.
             
             ** comments
             
             Lines starting with '#' can be processed like normal text or
             regarded as comments (option -m).  If regarded as comments, they
             may be printed (option -p) or suppressed.
             
             ** lists
             
             Lines starting with a single '-' or '+' are interpreted as items of a
             bulleted list.
                          
             Lines starting with "i." for an i >= 0 are interpreted
             as items of a numbered list.  The i value of the first such item
             determines the list's first number.  All subsequent items are
             numbered automatically.

             Finally, if a line starting with '-' or '+' contains " :: ", a
             dictionary list is created.  Each item in such a list is composed
             of a key (everything before the " :: ") and a description of the
             key (everything after the " :: ").
             
             For example, the following input:
             
             >>
             """
    text = """\
1. first item
1. A long item to show that list items are
formatted like
paragraphs as well.  That means, lines are
filled or wrapped to
fit the maximum line width.

1. third item

- This starts a new list.
+ second item of the new list

- third item of the new list
0.  This starts a new numbered list that counts
from 0.

9. This item's number is not 9.

And this is a dictionary:

- hat :: A covering for the head that is not
part of a piece of clothing.
          
+ shoe\t::\tA covering for the foot, usually
made of a strong material
such as leather, with a thick leather or
plastic sole and a heel.
- trousers (US pants) :: A piece of clothing that covers
the lower part of the body
from the waist to the feet.

+ glove :: A covering for the hand.

This is unrelated text to show how Outliner goes back to
paragraph mode when a list ends."""

    OL.verbatim(text)

    OL << """<<
             produces:"""

    OL << text

#_printOutlineHelp


class CommandLineParser:

    def __init__(self):
        self.appDescription = "Formats text for display on the screen. " \
                              "Reads from STDIN and writes to STDOUT."
    #__init__


    def parseCommandLine(self) -> argparse.Namespace:
        """
        Returns an argparse.Namespace with the following attributes:

          - action:          'a', 'f' or 'o'
          - align:           'l', 'r' or 'c' (only if action is 'a' or 'f')
          - lineWidth:       int (only if action is 'f' or 'o')
          - lvlWidth:        int (only if action is 'o')
          - processComments: bool (only if action is 'o')
          - printComments:   bool (only if action is 'o')
          - boldHeadings:    bool (only if action is 'o')
        """
        P = argparse.ArgumentParser(description=self.appDescription,
                                    add_help=True)
        P.add_argument("--version",
                       action="version",
                       version=__versionString__
                       )
        G1 = P.add_argument_group("actions")
        G1 = G1.add_mutually_exclusive_group()
        G1.add_argument("-a",
                        action="store_true",
                        help="only align lines, preserving original line "
                             "breaks (default)."
                        )
        G1.add_argument("-F",
                        metavar="LINE_WIDTH",
                        type=int,
                        help="preserve paragraph breaks, but fill text "
                             "with a maximum line width of LINE_WIDTH "
                             "characters.  LINE_WIDTH must be >= 10."
                        )
        G1.add_argument("-f",
                        dest="F",
                        action="store_const",
                        const=70,
                        help="equals -F 70"
                        )
        G1.add_argument("-O",
                        metavar="LINE_WIDTH",
                        type=int,
                        help="interpret input like Outliner Markup "
                             "and produce output with a maximum line width of "
                             "LINE_WIDTH characters. LINE_WIDTH must be >= 10. "
                             ""
                        )
        G1.add_argument("-o",
                        dest="O",
                        action="store_const",
                        const=70,
                        help="equals -O 70"
                        )
        G2 = P.add_argument_group("alignment")
        G2 = G2.add_mutually_exclusive_group()
        G2.add_argument("-l",
                        dest="align",
                        action="store_const",
                        const='l',
                        help="left (default)"
                        )
        G2.add_argument("-r",
                        dest="align",
                        action="store_const",
                        const='r',
                        help="right"
                        )
        G2.add_argument("-c",
                        dest="align",
                        action="store_const",
                        const='c',
                        help="centre"
                        )
        G3 = P.add_argument_group("outliner options")
        G3.add_argument("-H", "--o-help",
                        dest="ohelp",
                        action="store_true",
                        help="show extended help on option '-O' and exit"
                        )
        G3.add_argument("-m",
                        dest="processComments",
                        action="store_true",
                        help="regard lines starting with '#' as comments. "
                             "Without this flag, lines starting with '#' "
                             "are processed like normal input lines."
                        )
        G3.add_argument("-p",
                        dest="printComments",
                        action="store_true",
                        help="print comment lines (as comments).  Implies -m."
                        )
        G3.add_argument("-w",
                        metavar="LEVEL_WIDTH",
                        dest="lvlWidth",
                        type=int,
                        help="number of spaces per indentation level "
                             "(default = 4)"
                        )
        G3.add_argument("-b",
                        dest="boldHeadings",
                        action="store_false",
                        help="don't use ANSI escape codes. "
                             "Without this flag, ANSI codes are used to print "
                             "bold headings."
                        )
        A = P.parse_args()

        if A.ohelp:
            _printOutlineHelp()
            sys.exit(0)
        #if
        delattr(A, 'ohelp')

        if A.a or (A.F is None and A.O is None):
            setattr(A, 'action', 'a')
        elif A.F is not None:
            setattr(A, 'action', 'f')
            setattr(A, 'lineWidth', A.F)
        elif A.O is not None:
            setattr(A, 'action', 'o')
            setattr(A, 'lineWidth', A.O)
        #elif
        delattr(A, 'a')
        delattr(A, 'F')
        delattr(A, 'O')

        if A.action in ['f', 'o'] and A.lineWidth < 10:
            P.error("LINE_WIDTH must be >= 10")
        #if

        argError = lambda *opts: P.error("argument -%s: not allowed with argument -%s"
                                         % opts)
        if A.action in ['a', 'f']:
            if A.processComments:
                argError('m', A.action)
            #if
            if A.printComments:
                argError('p', A.action)
            #if
            if A.lvlWidth is not None:
                argError('w', A.action)
            #if
            delattr(A, 'boldHeadings')
        else: # A.action == 'o'
            if A.align is not None:
                argError(A.align, 'O')
            #if
            delattr(A, 'align')
            if A.printComments:
                A.processComments = True
            #if
            if A.lvlWidth is None:
                A.lvlWidth = 4
            #if
            if A.lvlWidth < 0:
                P.error("LEVEL_WIDTH must be >= 0")
            #if
        #else

        if A.action in ['a', 'f']:
            if A.align is None:
                A.align = 'l'
            #if
            delattr(A, 'printComments')
            delattr(A, 'processComments')
            delattr(A, 'lvlWidth')
        #if

        return A
    #parseCommandLine

#CommandLineParser


### aczutro ###################################################################
