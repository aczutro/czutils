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
"Private" help classes and functions used by module app.fill.
"""
from . import __versionString__

from ..utils import czcode

import argparse


@czcode.autoStr
class Args:
    """
    Bundles all inputs for app.fill.fill.
    """
    def __init__(self):
        self.action = ''
        self.align = ''
        self.lineWidth = 0
        self.tabWidth = 0
        self.fixSentenceEndings = 0
    # __init__
#Inputs


class CommandLineParser:

    def __init__(self):
        self.appDescription = "Reformats text read from STDIN and prints it "\
                              "to STDOUT."
    #__init__

    def parseCommandLine(self, lineWidth: int) -> Args:
        """
        Parses command line.

        :param lineWidth: Minimum value for option '-f'

        :returns: All arguments and flags bundled in an Args object.
        """
        P = argparse.ArgumentParser(description=self.appDescription,
                                    add_help=True)
        P.add_argument("--version",
                       action="version",
                       version=__versionString__
                       )
        G1 = P.add_argument_group("actions")
        G1 = G1.add_mutually_exclusive_group()
        G1.add_argument("-p",
                        action="store_true",
                        help="preserve original line breaks (default)"
                        )
        G1.add_argument("-F",
                        dest="LINE_WIDTH",
                        type=int,
                        help="fill text, i.e. wrap the text such that all " \
                             "lines are as full as possible, but not longer " \
                             "than LINE_WIDTH characters.  Preserves " \
                             "paragraph breaks.  LINE_WIDTH must be >= %d."
                             % lineWidth
                        )
        G1.add_argument("-f",
                        action="store_true",
                        help="equals -F 70"
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
        G3 = P.add_argument_group("other options")
        G3.add_argument("-t",
                        dest="TAB_WIDTH",
                        type=int,
                        default=1,
                        help="If not 0, replace tabs by this many spaces. "
                             "Default: 1."
                        )
        G3.add_argument("-n", "--no-2",
                        dest="fixSentenceEndings",
                        action="store_false",
                        help="Without this flag, makes sure that periods that "
                             "end a sentence are followed by exactly 2 spaces. "
                        )
        container = P.parse_args()

        ans = Args()

        if container.p:
            ans.action = 'p'
            ans.lineWidth = None
        elif container.LINE_WIDTH is not None:
            ans.action = 'f'
            ans.lineWidth = container.LINE_WIDTH
            if ans.lineWidth < lineWidth:
                P.error("LINE_WIDTH must be >= %d" % lineWidth)
            #if
        elif container.f:
            ans.action = 'f'
            ans.lineWidth = 70
        else:
            ans.action = 'p'
            ans.lineWidth = None
        #else

        if container.align is None:
            ans.align = 'l'
        else:
            ans.align = container.align
        #else

        if container.TAB_WIDTH < 0:
            P.error("TAB_WIDTH must be >= 0")
        else:
            ans.tabWidth = container.TAB_WIDTH
        #else

        ans.fixSentenceEndings = container.fixSentenceEndings

        return ans
    #parseCommandLine

#CommandLineParser


### aczutro ###################################################################
