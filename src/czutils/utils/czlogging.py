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


class LoggingChannel:
    """
    A logging channel that uses the standard python logger.

    The main differences to the standard logger are that only the methods
    info(), warning() and error() are provided, and that these methods
    concatenate all their arguments into one message, like print(...) does.

    Also, each instance has its own logging level so that logging can be turned
    on/off for individual modules or classes
    """

    def __init__(self, channelName: str, minLevel: int):
        """
        :param channelName: e.g. the application name
        :param minLevel:    minimum logging level.  If None, nothing is logged.
                            Possible values:
                              - LoggingLevel.INFO
                              - LoggingLevel.WARNING
                              - LoggingLevel.ERROR
                              - LoggingLevel.SILENT
        """
        logging.basicConfig(format="%(name)s: %(cln)s: %(message)s", # cln = custom level name
                            level="INFO")
        self._logger = logging.getLogger(channelName)
        self._level = LoggingLevel.SILENT if minLevel is None else minLevel
    #__init__


    def info(self, *args):
        """
        Logs a message with INFO level.
        """
        if self._level <= LoggingLevel.INFO:
            self._logger.info(' '.join((str(arg) for arg in args)),
                              extra={ "cln" : "info" })
        #if
    #info


    def warning(self, *args):
        """
        Logs a message with WARNING level.
        """
        if self._level <= LoggingLevel.WARNING:
            self._logger.warning(' '.join((str(arg) for arg in args)),
                                 extra={ "cln" : "warning" })
        #if
    #warning


    def error(self, *args):
        """
        Logs a message with ERROR level.
        """
        if self._level <= LoggingLevel.ERROR:
            self._logger.error(' '.join((str(arg) for arg in args)),
                               extra={ "cln" : "error" })
        #if
    #error

#LoggingChannel


### aczutro ###################################################################
