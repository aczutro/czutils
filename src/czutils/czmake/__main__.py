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
Turns a plain list of commands into a Makefile.
"""
from .czmake import CommandLineParser

from ..lib import czlogging, czsystem

import os.path
import sys


class CZMakeError(Exception):
    """
    Exception raised by function czmake.
    """
    pass
#CZMakeError


def czmake(inputFile: str = None,
           targetDir: str = ".",
           overwrite: bool = False,
           preserve: bool = False) -> int:
    """
    Reads a plain list of shell commands either from file or from sys.stdin
    and creates a 'Makefile' in which each command is an individual target.

    All targets are invoked by the 'all' target, so a call to "make [all]" will
    execute all commands and create an individual log file for each command.
    The 'Makefile' is formulated such that a second call to "make" will execute
    only the commands that failed the first time.

    The 'Makefile' also includes a 'clean' target that will remove the original
    input file, the 'Makefile' itself, and all the log files.

    Each input line is interpreted as an individual command.
    Lines starting with # are regarded as comments.

    :param inputFile: Path to file containing shell commands.
                      If it is None, reads from sys.stdin.
    :param targetDir: Path to directory where target and log files are to be
                      stored.  If a file or directory with that name already
                      exists, raises CZMakeError.
    :param overwrite: If true, overwrites file 'Makefile' silently.
                        If false and 'Makefile' already exists,
                      raises CZMakeError.
                        Does not apply to 'targetDir'.
    :param preserve:  If true, preserves input file, i.e. 'make clean' will not
                      delete it.

    :returns: 0 on success.

    :raises: CZMakeError
    :raises: czmake does NOT catch exceptions raised by OS-interacting functions
             like os.mkdir or io.open.
    """

    commands = []

    if inputFile is None:
        inputFile = ""
        commands = sys.stdin.read().splitlines()
    else:
        with open(inputFile, "r") as fileHandle:
            commands = fileHandle.read().splitlines()
        #with
    #else

    if preserve:
        inputFile = ""
    #if

    makefile = "Makefile"
    if os.path.exists(makefile) and not overwrite:
        raise CZMakeError("Can't overwrite '%s'." % makefile)
    #if

    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    elif not os.path.isdir(targetDir):
        raise CZMakeError("can't create log file directory '%s': "
                          "a non-directory with that name already exists" % targetDir)
    #if

    with open(makefile, "w") as makefileHandle:
        write = lambda msg : print(msg, file=makefileHandle)

        write("first: all")
        write("")

        targets = []
        logs = []

        targetCounter = 1
        for command in commands:
            command = command.lstrip(" \t")

            if not command or command[0] == '#':
                continue
            #if

            target = os.path.join(targetDir, "%03d" % targetCounter)
            targets.append(target)

            log = target + ".log"
            logs.append(log)

            write("%s:" % target)
            write("\t(%s && touch %s) 2>&1 | tee %s" % (command, target, log))
            write("")

            targetCounter += 1
        #for

        if os.path.samefile(targetDir, os.getcwd()):
            targetDir = ' '.join(targets + logs)
        #if

        write("all: %s" % " ".join(targets))
        write("")
        write(".PHONY: clean")
        write("")
        write("clean:")
        write("\trm -rf %s %s %s" % (targetDir, inputFile, makefile))
    #with

    return 0
#czmake


def main():
    """
    Main routine for command-line app czmake.
    """
    L = czlogging.LoggingChannel(czsystem.appName(),
                                 czlogging.LoggingLevel.WARNING)
    try:
        CLP = CommandLineParser()
        args = CLP.parseCommandLine()
        L.info(args)
        sys.exit(czmake(inputFile=args.inputFile,
                        targetDir=args.logDir,
                        overwrite=args.overwrite,
                        preserve=args.preserve
                        ))
    except AssertionError as e:
        raise e
    except CZMakeError as e:
        L.error(e)
        sys.exit(1)
    except Exception as e:
        L.error(e)
        sys.exit(2)
    #except
#main


if __name__ == '__main__':
    main()
#if


### aczutro ###################################################################
