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
Function to hide and "unhide" files.
"""
from pathlib import Path

from .clp import Args
from ..lib import czsystem, czuioutput

import shutil


class Breaker(Exception):
    """
    Raised to jump out of deep loops.
    """
    pass
#Breaker


def hideUnhide(args: Args,
               uiChannel : czuioutput.OutputChannel = czuioutput.DumbOutputChannel(),
               ) -> int:
    """
    Hides or "unhides" files, directories and symlinks.

    :param args:      Contains the following attributes:
                      files:       List of strings: each string is a path to a file,
                                   directory or symlink.
                      bHide:        If true, hides files.  If false, unhides them.
                      copy:        If true, instead of renaming the file, makes a
                                   hidden/unhidden copy.
                      strict:      In hide mode: If true, refuses to "hide hidden
                                   files".
                                   (If false, hiding ".file" means renaming it to
                                   "..file".)
                                   In unhide mode: If true, "completely unhides" files,
                                   i.e. "..file" becomes "file".  (If false, "..file"
                                   becomes ".file".)
                      abort:       If true, aborts on first failure.
                      noOverwrite: If false, silently overwrite target files (but not
                                   directories).
                      verbose:     If true, prints executed rename/copy operations to
                                   sys.stdout.

    :param uiChannel: An output channel for warnings and errors.

    :return: 0 on success, 1 on fail.  Fail means that at least one rename/copy
             operation has failed.

    :raises: ValueError
    :raises: hideUnhide does NOT catch exceptions raised by OS-interacting
             functions like shutil.copy2, shutil.copytree or os.replace.
    """
    if args.hide is None:
        raise ValueError("'args.hide' must not be None")
    #if

    if args.abort:
        fComplain = uiChannel.error
    else:
        fComplain = uiChannel.warning
    #else

    if args.copy:
        fRename = (lambda _src, _dst: shutil.copy2(_src, _dst,
                                                   follow_symlinks=False,
                                                   ),
                   lambda _src, _dst: shutil.copytree(_src, _dst,
                                                      symlinks=True,
                                                      ignore_dangling_symlinks=True,
                                                      )
                   )
    else:
        fRename = (lambda _src, _dst: _src.replace(_dst),
                   lambda _src, _dst: _src.replace(_dst),
                   )
    #else

    exitCode = 0

    for src in args.files:
        srcPath = Path(src)

        try:
            if srcPath.resolve() in (Path("/"),
                                     Path(".").resolve(),
                                     Path("..").resolve(),
                                     ):
                fComplain(f"you don't want to operate on '{srcPath}'"
                          f"{'' if args.abort else ' -- skipping'}")
                raise Breaker()
            #if
            if not srcPath.exists():
                fComplain(f"'{srcPath}' doesn't exist")
                raise Breaker()
            #if

            filename = srcPath.name
            newName = None
            if args.hide:
                if filename[0] != '.' or not args.strict:
                    newName = f".{filename}"
                #if
            else:
                if filename[0] == '.':
                    if args.strict:
                        newName = filename.strip('.')
                    else:
                        newName = filename[1:]
                    #else
                #if
            #else
            if newName is None:
                fComplain(f"'{src}' is {'already' if args.hide else 'not'} hidden")
                raise Breaker()
            #if

            dstPath = srcPath.parent / newName
            if dstPath.exists() and (args.noOverwrite or czsystem.isProperDir(dstPath)):
                skipping = "" if args.abort else f" -- skipping '{srcPath}'"
                fComplain(f"destination '{dstPath}' already exists{skipping}")
                raise Breaker()
            #if

            fRename[int(czsystem.isProperDir(src))](srcPath, dstPath)

            if args.verbose:
                print(f"'{srcPath}' -> '{srcPath.parent / dstPath.name}'")
            #if
        except Breaker:
            if args.abort:
                return 1
            else:
                exitCode = 1
            #else
        #except
    #for

    return exitCode
#hideUnhide


### aczutro ###################################################################
