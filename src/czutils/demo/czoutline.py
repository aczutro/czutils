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

"""Demo of module 'lib.czoutline'."""

from ..lib import czoutline, cztext


def demo():
    """
    Demo of module 'lib.czoutline'.
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
             indentation level of the headings that precede them.  This all
             happens automatically and you don't have to worry about it.
             However, sometimes it may be useful to increment the indentation of
             a paragraph.  The current indentation level can be incremented with
             "OL.inc()" and decremented with "OL.dec()"."""

    OL.dec()
    OL << """"OL << text" can be used to print a paragraph of text. 
             Paragraphs are not only indented automatically, but also formatted
             to fit the maximum line width.

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
    OL.verbatim('OL << """' + text + '"""')

    OL.dec()
    OL << "That command produces this:"

    OL.setLineWidth(60)
    OL << text
    OL.setLineWidth(70)

    OL << """>>
             "OL.verbatim(text)" prints the text as it is, which is how
               I printed the unprocessed Tom Sawyer text.
             Verbatim is useful when you have a good reason not to let Outliner
              wrap the lines, but note that verbatim sections are indented to
              match the document's indentation level.

             For example, let me print a colour chart
             that shouldn't be formatted
             like normal text:"""

    OL.verbatim(cztext.getPalette(cztext.Palette.COL16))

    OL << """Lists can be produced as well.  "OL.ul()" starts a bulleted
             list, and each list item is put with "OL.li(text)"."""

    OL.ul()
    OL.li("first item")
    OL.li("second item")
    OL.li("A long item to show that list items are formatted like "
          "paragraphs as well.  That means, lines are filled or wrapped to "
          " fit the "
          "maximum line width.")

    OL << """"OL.ol()" produces a numbered list."""

    OL.ol()
    OL.li("first item")
    OL.li("second item")
    OL.li("A long item to show that list items are formatted like "
          "paragraphs as well.  That means, lines are filled or wrapped to "
          " fit the "
          "maximum line width.")

    OL << """"OL.dl()" produces a dictionary list.  Each item is
          composed of a key and a description.  These are put with
          "OL.di(key, description)"."""

    OL.dl()
    OL.di("hat",
          "A covering for the head that is not part of a piece of clothing."
          )
    OL.di("shoe",
          """A covering for the foot, usually made of a strong material
          such as leather, with a thick leather or plastic sole and a
          heel."""
          )
    OL.di("trousers (US pants)",
          """A piece of clothing that covers the lower part of the body
          from the waist to the feet."""
          )
    OL.di("a truly splendid three-piece suit combined with shiny shoes "
          "and an elegant hat",
          "Just to see what happens with long keys."
          )

    OL << "This is unrelated text to show how Outliner " \
          "goes back to  paragraph mode  when no more list items are added."
#demo


### aczutro ###################################################################
