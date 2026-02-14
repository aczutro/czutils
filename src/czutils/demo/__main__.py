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
Demo application to show the capabilities of library 'czutils'.
"""

from . import czmath, czoutline, cztext, czthreading, czuioutput
from .. import __version__
from ..lib import czoutline as libczoutline

import argparse
import sys


def main():
    """
    Main routine for command-line app 'czutils-demo'.
    """
    P = argparse.ArgumentParser(description="Demo application to illustrate the "
                                            "capabilities of library czutils.",
                                add_help=True)
    P.add_argument("--version",
                   action="version",
                   version=f"czutils version {__version__}"
                   )
    G1 = P.add_argument_group()
    G1 = G1.add_mutually_exclusive_group()
    G1.add_argument("-all",       help="run all demos",        action="store_true")
    G1.add_argument("-uioutput",  help="run uioutput demo",    action="store_true")
    G1.add_argument("-math",      help="run czmath demo",      action="store_true")
    G1.add_argument("-outline",   help="run czoutline demo",   action="store_true")
    G1.add_argument("-text",      help="run cztext demo",      action="store_true")
    G1.add_argument("-threading", help="run czthreading demo", action="store_true")

    A = P.parse_args()

    if A.all:
        OL = libczoutline.Outliner()
        sep = lambda : OL.h1(
            "===============================================================================")
        czuioutput.demo()
        sep()
        czmath.demo()
        sep()
        czoutline.demo()
        sep()
        cztext.demo()
        sep()
        czthreading.demo()
    elif A.uioutput:
        czuioutput.demo()
    elif A.math:
        czmath.demo()
    elif A.outline:
        czoutline.demo()
    elif A.text:
        cztext.demo()
    elif A.threading:
        czthreading.demo()
    else:
        P.print_help()
    #else

    sys.exit(0)
#main


if __name__ == '__main__':
    main()
#if


### aczutro ###################################################################
