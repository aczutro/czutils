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

from . import __version__, __author__

import logging


class LogLevel:
    '''
    "Enum class" to categorise logging levels.
    '''
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
#LogLevel


class LogChannel:
    """
    A logging channel that uses the system logger.

    The main difference to the standard logger is that it only provides methods
    log, warning and error, and that these concatenate all their arguments into
    one message, like print(...) does.  For example:

    ::

        if not isinstance(someObject, int):
            channel.error("expected int, but got", someObject)
    """

    def __init__(self, channelName: str, minLevel: str = LogLevel.WARNING):
        """
        :param channelName: e.g. the application name
        :param minLevel:    minimum logging level.
                            Possible values:
                              - LogLevel.INFO
                              - LogLevel.WARNING
                              - LogLevel.ERROR
        """
        logging.basicConfig(format="%(name)s: %(cln)s: %(message)s", # cln = custom level name
                            level=minLevel)
        self.logger = logging.getLogger(channelName)
    #__init__


    def info(self, *args):
        """
        Logs a message with INFO level.
        """
        self._log(self.logger.info,
                  ' '.join((str(arg) for arg in args)),
                  "info")
    #info


    def warning(self, *args):
        """
        Logs a message with WARNING level.
        """
        self._log(self.logger.warning,
                  ' '.join((str(arg) for arg in args)),
                  "warning")
    #warning


    def error(self, *args):
        """
        Logs a message with ERROR level.
        """
        self._log(self.logger.error,
                  ' '.join((str(arg) for arg in args)),
                  "error")
    #error


    def _log(self, f, msg: str, levelName: str):
        """
        Back-end for logging functions.

        :param f:         pointer to logging function
        :param msg:       message to log
        :param levelName: custom level name to appear in message
        """
        f(msg, extra={ "cln" : levelName }) # cln = custom level name
    #_log

#LogChannel


### aczutro ###################################################################
