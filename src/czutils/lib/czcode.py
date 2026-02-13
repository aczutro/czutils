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

"""Help functions for code generation."""


def autoStr(cls):
    """
    Decorator: auto-generates __str__ method for the given class.
    """
    cls.__str__ = lambda self : \
        "%s { %s }" \
        % (type(self).__name__,
           ", ".join("%s = %s" % dictEntry for dictEntry in vars(self).items()))
    return cls
#autoStr


### aczutro ###################################################################
