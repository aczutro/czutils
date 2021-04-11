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

"""Library back-end of apps hide and uhide."""

from . import __version__, __author__

from .utils import czcode
from .utils import czlogging
from .utils import czsystem

import argparse
import shutil
import os
import os.path


@czcode.autoStr
class Flags:
    """
    Data structure for CommandLineParser.
    """
    def __init__(self):
        self.hide = None
        self.copy = False
        self.strict = False
        self.abort = False
        self.noOverwrite = False
        self.verbose = False
    # __init__
#Flags


class CommandLineParser:
    """
    Base class for command line parsing.
    """
    def __init__(self):
        self.hideMode = None
        self.appDescription = ""
        self.helpArgs = ""
        self.helpCopy = ""
        self.helpStrict = ""
        self.helpAbort = "Abort on first failure."
        self.helpOverwrite = "Overwrite mode: if a file with the target name "\
                             "already exists, overwrite it without warning. "\
                             "Does not apply to directories."
        self.helpVerbose = "Be verbose."
    # __init__

    def parseCommandLine(self):
        """
        Parses command line.

        :return: tuple: ( list of files, Flags object )
        """
        P = argparse.ArgumentParser(description=self.appDescription,
                                    add_help=True)
        versionString = "%%(prog)s %s" % __version__
        P.add_argument("--version",
                       action="version",
                       version=versionString
                       )
        P.add_argument("FILE",
                       type=str,
                       nargs='+',
                       help=self.helpArgs
                       )
        P.add_argument("-c",
                       dest="copy",
                       action="store_true",
                       help=self.helpCopy
                       )
        P.add_argument("-s",
                       dest="strict",
                       action="store_true",
                       help=self.helpStrict
        )
        P.add_argument("-a",
                       dest="abort",
                       action="store_true",
                       help=self.helpAbort
        )
        P.add_argument("-o",
                       dest="noOverwrite",
                       action="store_false",
                       help=self.helpOverwrite
        )
        P.add_argument("-v",
                       dest="verbose",
                       action="store_true",
                       help=self.helpVerbose
        )

        container = P.parse_args()

        flags = Flags()
        flags.hide = self.hideMode
        flags.copy = container.copy
        flags.strict = container.strict
        flags.abort = container.abort
        flags.noOverwrite = container.noOverwrite
        flags.verbose = container.verbose

        return container.FILE, flags

    #def parse_args

# CommandLineParser


class CLPHide(CommandLineParser):
    """
    Command line parser for hide.
    """
    def __init__(self):
        super().__init__()
        self.hideMode = True
        self.appDescription = "Prepends a dot to the basename of each "\
                              "file/directory/symlink."
        self.helpArgs = "File/directory/symlink to hide."
        self.helpCopy = "Instead of hiding the file, make a hidden copy of it."
        self.helpStrict = "Be strict, i.e. fail if the file is already hidden. "\
                          "Otherwise, prepend a dot to the file's name in any "\
                          "case, i.e. the file name may end up having multiple dots."
    #__init__

#CLPHide


class CLPUhide(CommandLineParser):
    """
    Command line parser for uhide.
    """
    def __init__(self):
        super().__init__()
        self.hideMode = False
        self.appDescription = "Removes the prefix dot from the basename of each "\
                              "file/directory/symlink."
        self.helpArgs = 'File/directory/symlink to "unhide".'
        self.helpCopy = "Instead of unhiding the file, make an unhidden copy of it."
        self.helpStrict = "Be strict, i.e. unhide the file in any case, "\
                          "i.e. remove all prefix dots from the file name. "\
                          "Otherwise, remove only one dot."
    #__init__

#CLPUhide


class Breaker(Exception):
    """
    Used by _execute to jump out of nested loops.
    """
    pass
#Breaker


def _isProperDir(directory: str):
    """
    :param directory: path to a directory

    :return: True iff directory is an actual directory, and not just a
             soft link to a directory.
    """
    return os.path.isdir(directory) and not os.path.islink(directory)
#_isProperDir


def _execute(files: list, flags: Flags, fWarning, fError) -> int:
    """
    Executes hiding/unhiding commands.

    :param files:    list of files to hide/unhide
    :param flags:    flag structure
    :param fWarning: pointer to function to log warning
    :param fError:   pointer to function to log error

    :return: 0 on success, 1 on fail.

    :raise: AssertionError and exceptions raised by os functions
    """
    assert flags.hide is not None

    nibbles = []
    if flags.hide:
        nibbles.append('already') # [0]
    else:
        nibbles.append('not') # [0]
    #else
    if flags.abort:
        fComplain = fError
        nibbles.append('') # [1]
        nibbles.append(lambda x: '') # [2]
    else:
        fComplain = fWarning
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
        src.rstrip(os.sep)
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
            if os.path.exists(dst) and (flags.noOverwrite or _isProperDir(dst)):
                fComplain("destination '%s' already exists" % dst, nibbles[2](src))
                raise Breaker()
            #if

            fRename[int(_isProperDir(src))](src, dst) # this may raise exceptions
                                                      # that will be caught by
                                                      # caller of this function
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
    Main routine for hide and uhide.

    :param CLPcls: command line parser class
    """
    L = czlogging.LogChannel(czsystem.appName(), czlogging.LogLevel.INFO)
    try:
        CLP = CLPcls()
        files, flags = CLP.parseCommandLine()
        L.info(files)
        L.info(flags)
        exit(_execute(files, flags, L.warning, L.error))
    except AssertionError as e:
        raise e
    except Exception as e:
        L.error(e)
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
