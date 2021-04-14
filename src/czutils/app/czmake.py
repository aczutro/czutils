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
from ..private.czmake import Inputs, CommandLineParser

from ..utils import czlogging
from ..utils import czsystem

import os.path
import sys


class CZMakeError(Exception):
    """
    Exception raised by function czmake.
    """
    pass
#HideUnhideException


def czmake(args: Inputs) -> int:
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

    The attributes of input are:

      - args.inputFile: str:  Path to file containing shell commands.
                              If it is '-', reads from sys.stdin.
      - args.targetDir: str:  Path to directory where log files are to be
                              stored.  If file or directory with that name
                              already exists, raises CZMakeError.
      - args.overwrite: bool: If true, overwrites file 'Makefile' silently.
                              If false and 'Makefile' already exists,
                              raises CZMakeError.
      - args.preserve: bool:  If true, preserves input file, i.e. 'make clean'
                              will not delete it.

    :param args: Data structure containing all inputs and flags.

    :return: 0 on success.

    :raises CZMakeException for usage errors.
            See description of input attributes.
    :raises czmake does NOT catch exceptions raised by OS-interacting functions
            like os.mkdir or io.open.
    """

    if args.inputFile == "-":
        args.inputFile = ""
        commands = sys.stdin.read().splitlines()
    else:
        with open(args.inputFile, "r") as fileHandle:
            commands = fileHandle.read().splitlines()
        #with
    #else

    if args.preserve:
        args.inputFile = ""
    #if

    if os.path.exists(args.targetDir):
        raise CZMakeError("can't create target dir %s: file/directory already exists" %
                          args.targetDir)
    #if

    makefile = "Makefile"
    if os.path.exists(makefile) and not args.overwrite:
        raise CZMakeError("Use '-o' if you want to overwrite %s." % makefile)
    #if

    os.mkdir(args.targetDir)

    with open(makefile, "w") as makefileHandle:
        write = lambda msg : print(msg, file=makefileHandle)

        write("first: all")
        write("")

        targets = []

        targetCounter = 1
        for command in commands:
            command = command.lstrip(" \t")

            if not command or command[0] == '#':
                continue
            #if

            target = os.path.join(args.targetDir, "%03d" % targetCounter)
            targets.append(target)

            log = target + ".log"

            write("%s:" % target)
            write("\t(%s && touch %s) 2>&1 | tee %s" % (command, target, log))
            write("")

            targetCounter += 1
        #for

        write("all: %s" % " ".join(targets))
        write("")
        write(".PHONY: clean")
        write("")
        write("clean:")
        write("\trm -rf %s %s %s" % (args.targetDir, args.inputFile, makefile))
    #with

    return 0
#czmake


def main():
    """
    Main routine for command-line app czmake.
    """
    L = czlogging.LogChannel(czsystem.appName())
    try:
        CLP = CommandLineParser()
        inputFile = CLP.parseCommandLine()
        L.info(inputFile)
        sys.exit(czmake(inputFile))
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


### aczutro ###################################################################
