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

"""A wrapper class for the system logger."""

import logging


class LoggingLevel:
    """
    IDs for logging levels.
    """
    INFO = 0
    WARNING = 1
    ERROR = 2
    SILENT = 3
#LoggingLevel


def _stringToColour(channelName: str) -> int:
    """
    :return: Returns a pseudo-random number between 31 and 36 depending on
             the value of channelName (deterministic).
    """
    return (sum([ ord(c) for c in channelName ] + [ 0 ] ) % 6) + 31
#_stringToColour

class LoggingChannel:
    """
    A logging channel that uses the standard python logger.

    The main differences to the standard logger are that only the methods
    info(), warning() and error() are provided, and that these methods
    concatenate all their arguments into one message, like print(...) does.

    Also, each instance has its own logging level so that logging can be turned
    on/off for individual modules or classes
    """

    def __init__(self, channelName: str, minLevel: int, colour = False):
        """
        :param channelName: e.g. the application name
        :param minLevel:    minimum logging level.  If None, nothing is logged.
                            Possible values:
                              - LoggingLevel.INFO
                              - LoggingLevel.WARNING
                              - LoggingLevel.ERROR
                              - LoggingLevel.SILENT
        :param colour:      If true, print channel name and level keyword in
                            colour.
        """
        # colour = colour on
        # cln = custom level name
        # def = colour off
        msgFormat = "%(colour)s%(name)s: %(bold)s%(cln)s:%(def)s %(message)s"
        logging.basicConfig(format = msgFormat, level = "INFO")

        self._logger = logging.getLogger(channelName)
        self._level = LoggingLevel.SILENT if minLevel is None else minLevel

        _colour = _stringToColour(channelName)
        _colourMap \
            = { "colour" : "\033[%dm" % _colour, "bold" : "", "def" : "\033[0m"} \
              if colour else { "colour" : "", "bold" : "", "def" : ""}

        self._infoMap = dict(_colourMap)
        self._warningMap = dict(_colourMap)
        self._errorMap = dict(_colourMap)

        self._infoMap.update({ "cln" : "info" })
        self._warningMap.update({ "cln" : "warning" })
        self._errorMap.update({ "cln" : "error" })
        if colour:
            self._errorMap.update({ "bold" : "\033[1m", "def" : "\033[0m"})
        #if
    #__init__


    def info(self, *args):
        """
        Logs a message with INFO level.
        """
        if self._level <= LoggingLevel.INFO:
            self._logger.info(' '.join((str(arg) for arg in args)),
                              extra = self._infoMap)
        #if
    #info


    def warning(self, *args):
        """
        Logs a message with WARNING level.
        """
        if self._level <= LoggingLevel.WARNING:
            self._logger.warning(' '.join((str(arg) for arg in args)),
                                 extra = self._warningMap)
        #if
    #warning


    def error(self, *args):
        """
        Logs a message with ERROR level.
        """
        if self._level <= LoggingLevel.ERROR:
            self._logger.error(' '.join((str(arg) for arg in args)),
                               extra = self._errorMap)
        #if
    #error

#LoggingChannel


### aczutro ###################################################################
