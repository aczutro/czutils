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

import time


class TimerType:
    """
    "Data type" for Timer.
    """
    WALLCLOCK, CPU = range(2)

    @staticmethod
    def invalid(type):
        """
        :returns: True if 'type' is not TimerType.WALLCLOCK or TimerType.CPU.
        """
        return type not in range(2)
    #invalid

#TimerType


class TimerResolution:
    """
    "Data type" for Timer.
    """
    NS, S = range(2)


    @staticmethod
    def invalid(res):
        """
        :returns: True if 'res' is not TimerResolution.NS or TimerResolution.S.
        """
        return res not in range(2)
    #invalid

#TimerResolution


class Timer():
    """
    An easy-to-use timer.
    """

    def __init__(self,
                 type: TimerType = TimerType.CPU,
                 res: TimerResolution = TimerResolution.S):
        """
        :param type: If TimerType.WALLCLOCK, measured time is wall clock time.
                     If TimerType.CPU, measured time is CPU time.
        :param res:  If TimerResolution.NS, measured time is in NANOSECONDS
                     (int).
                     If TimerResolution.S, measured time is in SECONDS (float).
        """
        if (type, res) == (TimerType.WALLCLOCK, TimerResolution.S):
            self.f = time.time
        elif (type, res) == (TimerType.WALLCLOCK, TimerResolution.NS):
            self.f = time.time_ns
        elif (type, res) == (TimerType.CPU, TimerResolution.S):
            self.f = time.process_time
        elif (type, res) == (TimerType.CPU, TimerResolution.NS):
            self.f = time.process_time_ns
        elif TimerType.invalid(type):
            raise ValueError(
                "'type' must be TimerType.WALLCLOCK or TimerType.CPU")
        else:
            raise ValueError(
                "'res' must be TimerResolution.NS or TimerResolution.S")
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
