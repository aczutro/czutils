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
Main routines for apps 'hide' and 'uhide'.
"""
from .clp import CLPHide, CLPUhide
from .hide import hideUnhide
from ..lib import czuioutput

import logging
import sys


def _main(CLPcls):
    """
    Template for hide and uhide.

    :param CLPcls: command line parser class
    """
    logging.basicConfig(level=logging.CRITICAL)

    uiout = czuioutput.OutputChannel()

    CLP = CLPcls()
    args = CLP.parseCommandLine()
    logging.info(args)

    try:
        sys.exit(hideUnhide(args,
                            uiChannel=uiout,
                            )
                 )
    except ValueError as e:
        assert False, str(e)
    #except
#_main


def hide():
    """
    Main routine for command-line app 'hide'.
    """
    _main(CLPHide)
#hide


def uhide():
    """
    Main routine for command-line app 'uhide'.
    """
    _main(CLPUhide)
#uhide


if __name__ == '__main__':
    _uiout = czuioutput.OutputChannel()
    _uiout.error("This file cannot be executed directly. "
                 "It provides two main routines: 'hide' and 'uhide'.")
    sys.exit(3)
#if


### aczutro ###################################################################
