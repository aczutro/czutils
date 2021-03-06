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

"""Application package."""

from .. import __version__, __author__

from .demo import main as mainDemo
from .hide import mainHide, mainUhide
from .czmake import main as mainCZMake
from .textformat import main as mainTextFormat

### aczutro ###################################################################
