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

"""Demo of module 'lib.czthreading'."""

from ..lib import czoutline, czthreading

import random
import time


class Ping(czthreading.Message):
    pass
#Ping


class Pong(czthreading.Message):
    pass
#Pong


class Peng(czthreading.Message):
    pass
#Peng


class Player(czthreading.ReactiveThread):
    """
    Asynchronous component for 'lib.czthreading' demo.
    """
    def __init__(self, name: str, OL: czoutline.Outliner):
        super().__init__(name, None)
        self.addMessageProcessor("Ping", self.processPing)
        self.addMessageProcessor("Pong", self.processPong)
        self._otherPlayer = None
        self._OL = OL
    #__init__

    def setOtherPlayer(self, other: "Player"):
        self._otherPlayer = other
    #setOtherPlayer

    def processPing(self, message: czthreading.Message):
        self._OL << message.msgType()
        time.sleep(random.random())
        self._otherPlayer.comm(Pong())
    #processPing

    def processPong(self, message: czthreading.Message):
        self._OL << message.msgType()
        time.sleep(random.random())
        self._otherPlayer.comm(Ping())
    #processPong
#Player


def demo():
    """
    Demo of module 'lib.czthreading'.
    """
    OL = czoutline.Outliner()
    OL.h1("czthreading demo")

    p1 = Player("ping-player", OL)
    p2 = Player("pong-player", OL)
    p1.setOtherPlayer(p2)
    p2.setOtherPlayer(p1)
    p1.start()
    p2.start()

    OL << "Sending a Peng message to ping player.  It won't like that."

    p1.comm(Peng())
    time.sleep(1)

    OL << "Sending a Ping message to ping player.  It will like that."

    p1.comm(Ping())
    time.sleep(5)

    p1.comm(czthreading.QuitMessage())
    p2.comm(czthreading.QuitMessage())

    p1.wait()
    p2.wait()

    OL << "Killed both players."
#demo


### aczutro ###################################################################
