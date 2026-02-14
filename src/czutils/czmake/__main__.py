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
Turns a plain list of commands into a Makefile.
"""

from .clp import CommandLineParser
from .czmake import CZMakeError, czmake
from ..lib import czuioutput

import logging
import sys


def main():
    """
    Main routine for command-line app czmake.
    """
    logging.basicConfig(level=logging.CRITICAL)
    uiout = czuioutput.OutputChannel()

    try:
        clp = CommandLineParser()
        args = clp.parseCommandLine()
        logging.info(args)
        sys.exit(czmake(args))
    except CZMakeError as e:
        uiout.error(e)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(2)
    #except
#main


if __name__ == '__main__':
    main()
#if


### aczutro ###################################################################
