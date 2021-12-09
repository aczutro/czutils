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
Demo application to show the capabilities of library 'czutils'.
"""
from ..private import __versionString__
from ..utils import czoutline, cztext, czthreading, czlogging

import argparse
import random
import sys
import time


def czloggingDemo():
    """
    Demo of module 'utils.czlogging'.
    """
    OL = czoutline.Outliner()

    OL.h1("czlogging demo")

    OL.verbatim("")

    logger = czlogging.LoggingChannel("default logger",
                                      czlogging.LoggingLevel.INFO)
    logger.info("This is an info message.")
    logger.warning("This is a warning.")
    logger.error("This is an error message.")

    OL.verbatim("")

    logger = czlogging.LoggingChannel("colour logger",
                                      czlogging.LoggingLevel.INFO,
                                      colour=True)
    logger.info("This is an info message.")
    logger.warning("This is a warning.")
    logger.error("This is an error message.")


#czloggingDemo

def czoutlineDemo():
    """
    Demo of module 'utils.czoutline'.
    """
    OL = czoutline.Outliner()

    OL.h1("czoutline demo")

    OL << """Module 'czoutline' provides Class Outliner, which is a document
             formatter for text
             displayed on a purely text-based medium, like the
             command line terminal or the text editor."""

    OL << """The premise is that the text-based environment provides only one
             font size and very limited support for styles and colours.  Hence,
             structure is achieved solely through indentation."""

    OL << "Let OL = czoutline.Outliner()."

    OL << """OL.h1, OL.h2 and OL.h3 can be passed a single line of text to
             print level-1, level-2 or level-3 headings, respectively.
             For example, "OL.h1('level 1')" produces:"""

    OL.h1("level 1")

    OL << '''"OL.h2('a level-2 heading')" produces:'''

    OL.h2("a level-2 heading")

    OL << """And "OL.h3('a longer level-3 heading')" produces:"""

    OL.h3("a longer level-3 heading")

    OL << """Did you notice how the word "level" was written in all-caps
             in the level-1 heading, and how all the words were
             capitalised in the other two headings?
             And, if your console supports it, all three headings were shown in
             bold font or colour.  That's the basic styling this module offers.
             However, it's very easy to define your own styles."""

    OL << """For example, let's change the level-3 style with:"""

    OL.inc()
    OL << """OL.setH3Style(lambda s : "=== " + s + " ===")"""
    OL.dec()

    OL << """and print a level-3 heading with "OL.h3('example')":"""

    OL.setH3Style(lambda s : "=== " + s + " ===")
    OL.h3('example')

    OL << """As you may have noticed, paragraphs are indented to match the
             indentation level of the headings that precede them.  However, it
             is also possible to increment or decrement the 
             indentation level with "OL.inc()" and
             "OL.dec()", respectively.  That's useful, for example, to
             "highlight" statements, like I did with the setH3Style line of
             code."""

    OL.dec()
    OL << """"OL << text" can be used to print a paragraph of text. That's 
             what I've been using to print all the paragraphs you just 
             read.  The lines of the paragraph are automatically wrapped to fit
             the maximum line width. 
              
             However, "OL << text" can do a lot more than just print
             a single paragraph.  That function interprets certain
             patterns in 'text' as commands that will produce headings or
             manipulate the indentation level."""

    OL << "For example, have a look at this command: "

    text = """
     # -*- mode: org -*-
     #+TITLE:     Tom Sawyer
     #+AUTHOR:    Mark Twain
     #+EMAIL:     real.mark.twain@mississippi.com
     #+DATE:      Sat Aug 15 17:41:00 CDT 1874

     * ------------------------------------------------------------

     * the adventures of tom sawyer

     by Mark Twain (Samuel Langhorne Clemens)

     ** chapter 1

     "TOM!"

     No answer.

     "TOM!"

     No answer.

     "What's
     gone
     with
     that
      boy,
       I
       wonder?
       You,
        TOM!"

     No answer.

     >>

     [Place illustration here.]

     <<

     The old lady pulled her spectacles down and looked over them
      about the room;
      then she put them up and looked out under them.
     She seldom or never looked THROUGH them for so small a thing
      as a boy;
      they were her state pair, the pride of her heart, and
     were built for "style," not service -- she could have seen
      through a pair
      of stove-lids just as well. She looked perplexed for
     a moment, and then said, not fiercely, but still loud enough
      for the
      furniture to hear:

     * ------------------------------------------------------------
     """

    OL.inc()
    OL.verbatim('P << """' + text + '"""')

    OL.dec()
    OL << "That command produces this:"

    OL.setLineWidth(60)
    OL << text
    OL.setLineWidth(70)

    OL << """>>
             Finally, "OL.verbatim(text)" prints the text as it is, which is how
               I printed the unprocessed Tom Sawyer text.
             Verbatim is useful when you have a good reason not to let Outliner
              wrap the lines, but note that verbatim sections are indented to 
              match the document's indentation level.
              
             For example, let me print a colour chart
             that shouldn't be formatted
             like normal text:"""

    OL.verbatim(cztext.getPalette(cztext.Palette.COL16))

    OL << "* ==============================================================================="

#czoutlineDemo


def cztextDemo():
    """
    Demo of module 'utils.cztext'.
    """
    OL = czoutline.Outliner(h2Style=czoutline.Style.BOLD,
                            h3Style=czoutline.Style.BOLD)

    OL << """* cztext demo
             
             Module 'cztext' provides functions to format text that will be
             displayed on a purely text-based medium, like the 
             command line terminal or the text editor.
             
             ** cztext.colourise
             
             This function takes a string and returns a copy of it with ANSI
             escape codes that will make the text and its background have the
             chosen colours when printed on ANSI-compliant
             terminals.
             """

    OL << """Three colour palettes are supported.
             
             *** 16-colour palette
             """
    OL.verbatim(cztext.getPalette(cztext.Palette.COL16))

    OL << "*** 256-colour palette"
    OL.verbatim(cztext.getPalette(cztext.Palette.COL256))

    OL << "*** greyscale palette"
    OL.verbatim(cztext.getPalette(cztext.Palette.GREYSCALE))

    OL << """<<
             In addition, this function can manipulate several font properties:
             >>"""

    OL.verbatim([ cztext.colourise("This is bold text.", bold=True),
                  cztext.colourise("This is slanted text.", italics=True),
                  cztext.colourise("This is underlined text.", underline=True),
                  cztext.colourise("This is struck-through text.", strikethrough=True),
                  cztext.colourise("This is blinking text.", blinking=True),
                  cztext.colourise("Here, foreground and background colours are "
                                   "inverted.", inverted=True),
                  cztext.colourise("These properties can also be combined.",
                                   bold=True,
                                   italics=True,
                                   underline=True)
                  ])

    text = """It was seven o'clock of a very warm evening
 in the Seeonee hills
      when Father Wolf woke up from his day's rest,
              scratched himself, yawned, and spread out \t his 
paws one  after   the    other to get rid of the\tsleepy 
                       feeling in their tips. \t"""

    OL << """** cztext.align
             
             This function aligns text left, right or centre:
             
             Take, for example, this input text:
             
             >>
             """
    OL.verbatim(text)

    OL << "*** aligned left"
    OL.verbatim(cztext.align(text.splitlines(), 'l', collapseSpaces=True))

    OL << "*** aligned right"
    OL.verbatim(cztext.align(text.splitlines(), 'r', collapseSpaces=True))

    OL << "*** centered"
    OL.verbatim(cztext.align(text.splitlines(), 'c', collapseSpaces=True))

    OL << """** cztext.fill

             This function fills up all lines without exceeding a maximum line
             width.  For example:
             >>
             """

    l = lambda _b, _f, _w : [ cztext.colourise(line.ljust(_w),
                                              background=_b,
                                              foreground=_f,
                                              palette=cztext.Palette.COL256
                                              )
                             for line in cztext.fill(text, _w) ]

    OL.verbatim(l(229, 202, 60))
    OL.verbatim(l(195, 27, 40))
    OL.verbatim(l(194, 22, 20))

    OL << "* ==============================================================================="

#cztextDemo


class Ping(czthreading.Message):
    """Message class for utils.czthreading demo."""
    pass
#def

class Pong(czthreading.Message):
    """Message class for utils.czthreading demo."""
    pass
#def

class Peng(czthreading.Message):
    """Message class for utils.czthreading demo."""
    pass
#def

class Player(czthreading.ReactiveThread):
    """
    Asynchronous component for utils.czthreading demo.
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


def czthreadingDemo():
    """
    Demo of module 'utils.czthreading'.
    """
    OL = czoutline.Outliner()
    OL.h1("czthreading demo")

    czthreading.setLoggingOptions(czlogging.LoggingLevel.WARNING)

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

#czthreadingDemo


#czthreadingDemo


def main():
    """
    Main routine for command-line app 'czutils-demo'.
    """
    P = argparse.ArgumentParser(description="Demo application to illustrate the "
                                            "capabilities of library czutils.",
                                add_help=True)
    P.add_argument("--version",
                   action="version",
                   version=__versionString__
                   )
    G1 = P.add_argument_group()
    G1.add_argument("-all",
                    action="store_true",
                    help="run all demos"
                    )
    G2 = P.add_argument_group()
    G2 = G2.add_mutually_exclusive_group()

    aa = lambda o, h: G2.add_argument(o, action="store_true", help=h)
    aa("-logging", "run czlogging demo")
    aa("-outline", "run czoutline demo")
    aa("-text", "run cztext demo")
    aa("-threading", "run czthreading demo")
    A = P.parse_args()

    if A.all:
        czloggingDemo()
        czoutlineDemo()
        cztextDemo()
        czthreadingDemo()
    elif A.logging:
        czloggingDemo()
    elif A.outline:
        czoutlineDemo()
    elif A.text:
        cztextDemo()
    elif A.threading:
        czthreadingDemo()
    else:
        P.print_help()
    #else

    sys.exit(0)
#main


### aczutro ###################################################################
