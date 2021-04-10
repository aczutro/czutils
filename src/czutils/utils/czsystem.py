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

"""Help functions related to system environment."""


import os.path
import sys


def appName():
    """Returns the command that called the application.

    If it's a path, returns only the base name.
    """
    if len(sys.argv):
        return os.path.basename(sys.argv[0])
    else:
        return None
    #else
#appName


### aczutro ###################################################################
