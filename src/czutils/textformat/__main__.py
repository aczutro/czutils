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

from .clp import CommandLineParser
from .textformat import textFormat
from ..lib import czuioutput

import pprint
import logging
import sys


def main():
    """
    Main routine for command-line app 'textformat'.
    """
    logging.basicConfig(level=logging.CRITICAL)
    uiout = czuioutput.OutputChannel()

    CLP = CommandLineParser()
    args = CLP.parseCommandLine()
    logging.info(pprint.pformat(args))

    try:
        print(textFormat(sys.stdin.read(),
                         args
                         )
              )
    except ValueError as e:
        uiout.error(e)
        sys.exit(1)
    #except

    sys.exit(0)
#main


if __name__ == '__main__':
    main()
#if


### aczutro ###################################################################
