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
Function to hide and "unhide" files,
and main routines for applications hide and uhide.
"""
from ..private.hide import nop, Breaker, Flags, CLPHide, CLPUhide

from ..utils import czlogging
from ..utils import czsystem

import shutil
import os
import os.path
import sys


def hideUnhide(files: list, flags: Flags,
               logChannel: czlogging.LogChannel = None
               ) -> int:
    """
    Hides or "unhides" files, directories and symlinks.

    The attributes of the flag collection (all bool) determine the details of
    the process:

      - flags.hide:        If true, hide files.  If false, unhide them.
      - flags.copy:        If true, instead of renaming the file,
                           make a hidden/unhidden copy.
      - flags.strict:      In hide mode: If true, refuse to "hide hidden files".
                                         (If false, hiding ".file" means
                                         renaming it to "..file".)
                           In unhide mode: If true, "completely unhide" files,
                                           i.e. "..file" becomes "file".
                                           (If false, "..file" becomes ".file".)
      - flags.abort:       If true, abort on first failure.
      - flags.noOverwrite: If false, silently overwrite target files
                           (but not directories).
      - flags.verbose:     If true, be verbose (printed on sys.stdout).

    :param files:      list of files to hide or unhide
    :param flags:      collection of flags that control the process
    :param logChannel: a log channel for warnings and errors (optional)

    :return: 0 on success, 1 on fail.

    :raise: hideUnhide does NOT catch exceptions raised by OS-interacting
            functions like shutil.copy2, shutil.copytree or os.replace.
    """
    assert flags.hide is not None

    nibbles = []
    if flags.hide:
        nibbles.append('already') # [0]
    else:
        nibbles.append('not') # [0]
    #else
    if flags.abort:
        if logChannel is None:
            fComplain = nop
        else:
            fComplain = logChannel.error
        #else
        nibbles.append('') # [1]
        nibbles.append(lambda x: '') # [2]
    else:
        if logChannel is None:
            fComplain = nop
        else:
            fComplain = logChannel.warning
        #else
        nibbles.append('-- skipping') # [1]
        nibbles.append(lambda x: "-- skipping '%s'" % x) # [2]
    #else

    if flags.copy:
        fRename = (lambda _src, _dst: shutil.copy2(_src, _dst, follow_symlinks=False),
                   lambda _src, _dst: shutil.copytree(_src, _dst, symlinks=True,
                                                      ignore_dangling_symlinks=True)
                   )
    else:
        fRename = (lambda _src, _dst: os.replace(_src, _dst),
                   lambda _src, _dst: os.replace(_src, _dst)
                   )
    #else

    exitCode = 0

    for src in files:
        src = src.rstrip(os.sep)
        directory = os.path.dirname(src)
        filename = os.path.basename(src)

        try:
            if not src: # may occur if original argument was '/'
                fComplain("you don't want to operate on '/'", nibbles[1])
                raise Breaker()
            #if
            if filename in [ '.', '..' ]:
                fComplain("you don't want to operate on '%s'" % src, nibbles[1])
                raise Breaker()
            #if
            if not os.path.exists(src) and not os.path.islink(src):
                fComplain("file '%s' doesn't exist" % src)
                raise Breaker()
            #if

            newName = None
            if flags.hide:
                if filename[0] != '.' or not flags.strict:
                    newName = '.' + filename
                #if
            else:
                if filename[0] == '.':
                    if flags.strict:
                        newName = filename.strip('.')
                    else:
                        newName = filename[1:]
                    #else
                #if
            #else
            if newName is None:
                fComplain("file '%s' is" % src, nibbles[0], 'hidden')
                raise Breaker()
            #if

            dst = os.path.join(directory, newName)
            if os.path.exists(dst) and\
                    (flags.noOverwrite or czsystem.isProperDir(dst)):
                fComplain("destination '%s' already exists" % dst, nibbles[2](src))
                raise Breaker()
            #if

            fRename[int(czsystem.isProperDir(src))](src, dst)

            if flags.verbose:
                print("'%s' -> '%s'" % (src, dst))
            #if
        except Breaker:
            if flags.abort:
                return 1
            else:
                exitCode = 1
            #else
        #except
    #for

    return exitCode
#_execute


def _mainTemplate(CLPcls):
    """
    Template for mainHide and mainUhide.

    :param CLPcls: command line parser class
    """
    L = czlogging.LogChannel(czsystem.appName())
    try:
        CLP = CLPcls()
        files, flags = CLP.parseCommandLine()
        L.info(files)
        L.info(flags)
        sys.exit(hideUnhide(files, flags, L))
    except AssertionError as e:
        raise e
    except Exception as e:
        L.error(e)
        sys.exit(2)
    #except
#mainHide


def mainHide():
    """
    Main routine for command-line app hide.
    """
    _mainTemplate(CLPHide)
#mainHide


def mainUhide():
    """
    Main routine for command-line app uhide.
    """
    _mainTemplate(CLPUhide)
#mainUhide


### aczutro ###################################################################
