# Copyright (C) 2026 - present  Alexander Czutro <github@czutro.ch>
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

from .clp import Args

from pathlib import Path
import sys


class CZMakeError(Exception):
    """
    Exception raised by function czmake.
    """
    pass
#CZMakeError


def czmake(args: Args) -> int:
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

    :param args:    inputFile: Path to file containing shell commands.
                               If it is None, reads from sys.stdin.
                    targetDir: Path to directory where target and log files are
                               to be stored.  If a file or directory with that
                               name already exists, raises CZMakeError.
                    overwrite: If true, overwrites file 'Makefile' silently.
                               If false and 'Makefile' already exists,
                               raises CZMakeError.
                               Does not apply to 'targetDir'.
                    preserve:  If true, preserves input file, i.e. 'make clean'
                               will not delete it.

    :returns: 0 on success.

    :raises: CZMakeError
    :raises: czmake does NOT catch exceptions raised by OS-interacting functions
             like os.mkdir or io.open.
    """

    commands = []

    if args.inputFile is None:
        inputFile = ""
        commands = sys.stdin.read().splitlines()
    else:
        inputFile = str(args.inputFile)
        with open(args.inputFile, "r") as fileHandle:
            commands = fileHandle.read().splitlines()
        #with
    #else

    if args.preserve:
        inputFile = ""
    #if

    makefile = Path("Makefile")
    if makefile.exists() and not args.overwrite:
        raise CZMakeError(f"Can't overwrite '{makefile}'.")
    #if

    try:
        args.targetDir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise CZMakeError(e)
    #except

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

            target = args.targetDir / f"{targetCounter:03d}"
            targets.append(str(target))

            log = f"{target}.log"
            logs.append(log)

            write("%s:" % target)
            write("\t(%s && touch %s) 2>&1 | tee %s" % (command, target, log))
            write("")

            targetCounter += 1
        #for

        if args.targetDir.samefile(Path.cwd()):
            targetDir = ' '.join(targets + logs)
        else:
            targetDir = str(args.targetDir)
        #else

        write("all: %s" % " ".join(targets))
        write("")
        write(".PHONY: clean")
        write("")
        write("clean:")
        write(f"\trm -rf {targetDir} {inputFile} {makefile}")
    #with

    return 0
#czmake


### aczutro ###################################################################
