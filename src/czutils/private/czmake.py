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
"Private" help classes and functions for module app.czmake.
"""
from . import __versionString__

import argparse


class CommandLineParser:

    def __init__(self):
        self.appDescription = "Turns a plain list of commands into a Makefile. "\
                              "Each line is understood as a command. "\
                              "Lines starting with # are regarded as comments. "
    # __init__

    def parseCommandLine(self) -> argparse.Namespace:
        """
        Parses command line.

        :returns: All arguments and flags bundled in an Args object.
        """
        P = argparse.ArgumentParser(description=self.appDescription,
                                    add_help=True)
        P.add_argument("--version",
                       action="version",
                       version=__versionString__
                       )
        P.add_argument("inputFile",
                       metavar="INPUT_FILE",
                       type=str,
                       nargs='?',
                       help="File with a plain list of commands to execute. "
                            "If '-' or omitted, reads from STDIN."
                       )
        G1 = P.add_argument_group()
        G1.add_argument("-l",
                        metavar="LOG_DIR",
                        dest="logDir",
                        type=str,
                        default=".targets",
                        help="Store log files in this directory. "
                             " Default: '%(default)s'"
                        )
        G2 = P.add_argument_group()
        G2.add_argument("-o",
                        dest="overwrite",
                        action="store_true",
                        help="If file 'Makefile' exists, overwrite it silently."
                        )
        G2.add_argument("-p",
                        dest="preserve",
                        action="store_true",
                        help="Preserve input file, i.e. 'make clean' will not "
                             "delete it"
                        )
        container = P.parse_args()

        if container.inputFile == '-':
            container.inputFile = None
        #if

        return container

    #def parse_args

#CommandLineParser


### aczutro ###################################################################
