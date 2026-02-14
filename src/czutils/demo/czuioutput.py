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

"""Demo of module 'lib.czuioutput'."""

from ..lib import czoutline, czuioutput


def demo():
    """
    Demo of module 'lib.czuioutput'.
    """
    OL = czoutline.Outliner()

    OL.h1("czuioutput demo")

    OL.verbatim("")

    uiout = czuioutput.OutputChannel()
    uiout.info("This is an info message.")
    uiout.warning("This is a warning.")
    uiout.error("This is an error message.")
#demo


### aczutro ###################################################################
