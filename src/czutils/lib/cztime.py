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

"""An easy-to-use timer."""

import enum
import time


class TimerType(enum.Enum):
    WALLCLOCK = enum.auto()
    CPU = enum.auto()
#TimerType


class TimerResolution(enum.Enum):
    NS = enum.auto()
    S = enum.auto()
#TimerResolution


class Timer:
    """
    An easy-to-use timer.
    """

    def __init__(self,
                 timerType: TimerType = TimerType.CPU,
                 res: TimerResolution = TimerResolution.S):
        """
        :param timerType: If TimerType.WALLCLOCK, measured time is wall clock
                          time.
                          If TimerType.CPU, measured time is CPU time.

        :param res:       If TimerResolution.NS, measured time is in NANOSECONDS
                          (int).
                          If TimerResolution.S, measured time is in SECONDS
                          (float).
        """
        if (timerType, res) == (TimerType.WALLCLOCK, TimerResolution.S):
            self.f = time.time
        elif (timerType, res) == (TimerType.WALLCLOCK, TimerResolution.NS):
            self.f = time.time_ns
        elif (timerType, res) == (TimerType.CPU, TimerResolution.S):
            self.f = time.process_time
        elif (timerType, res) == (TimerType.CPU, TimerResolution.NS):
            self.f = time.process_time_ns
        else:
            assert False, "impossible value combination of TimerType and TimerResolution"
        #else

        self.start = self.f()
    #__init__


    def time(self):
        """
        :returns: The time elapsed since the instantiation of this Timer object.
        """
        return self.f() - self.start
    #time

#Timer


### aczutro ###################################################################
