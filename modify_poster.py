#!/usr/bin/env python
#
# Code to insert text in poster jpg files.
#
# Copyright: Surhud More (IUCAA) 2020
#
# Bug reports/comments: Open github issues, or send pull requests

import textwrap
from PIL import Image, ImageDraw, ImageFont
from os import path
import numpy as np
import sys
import pandas

class fill_poster:
    def __init__(self, image):
        self.imagename = image
        self.image = Image.open(image+".png")
        self.fullwidth = self.image.width

    def output_text(self, message, y, font=None, width=None, color='rgb(0, 0, 0)', offsety=30, printoffset=False):

        # This class will write out the line in the file in multiple lines and center it.
        for line in textwrap.wrap(message, width):
            w, h = self.draw.textsize(line, font=font)
            self.draw.text(((self.image.width-w)/2, y + offsety), line, font=font, fill=color)
            offsety += font.getsize(line)[1]

    def convert(self, ii, strings, pl, language, fonts):
        # Initiate image
        self.draw = ImageDraw.Draw(self.image)

        # Add a common The Hoaxbusters line
        #self.output_text("Frequently asked questions", 40, font=fonts["4"],  width=30)

        # Add all the strings at the right places with the right fonts
        self.output_text(strings[0], pl[0], font=fonts["1"], width=pl[4], color='rgb(94, 94, 94)')
        self.output_text(strings[1], pl[1], font=fonts["2"], width=pl[5])
        self.output_text(strings[2], pl[2], font=fonts["3"], width=pl[6], color='rgb(94, 94, 94)')
        self.output_text(strings[3], pl[3], font=fonts["4"], width=pl[7], color='rgb(189, 23, 23)')

        # Save the file
        self.image.save("Final/"+self.imagename.replace("blank-", "")+"_%s.png" % language)
