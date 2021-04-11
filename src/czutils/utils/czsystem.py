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

from . import __version__, __author__

import os.path
import sys


def appName() -> str:
    """
    :return: the basename of the command that started the running application.
    """
    if len(sys.argv):
        return os.path.basename(sys.argv[0])
    else:
        return None
    #else
#appName


### aczutro ###################################################################
