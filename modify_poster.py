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

    def output_text(self, message, y, font=None, width=None, color='rgb(0, 0, 0)', offsety=30, printoffset=False, offsetx=0):

        # This class will write out the line in the file in multiple lines and center it.
        for line in textwrap.wrap(message, width):
            w, h = self.draw.textsize(line, font=font)
            self.draw.text((offsetx+(self.image.width-w)/2, y + offsety), line, font=font, fill=color)
            offsety += font.getsize(line)[1]*1.2

    def convert(self, ii, strings, pl, language, fonts, delta=0):
        # Initiate image
        self.draw = ImageDraw.Draw(self.image)

        # Add a common The Hoaxbusters line
        #self.output_text("Frequently asked questions", 40, font=fonts["4"],  width=30)

        # Add all the strings at the right places with the right fonts
        self.output_text(strings[0], pl[0], font=fonts["1"], width=pl[7], color='rgb(94, 94, 94)')
        self.output_text(strings[1], pl[1], font=fonts["2"], width=pl[8])
        self.output_text(strings[2], pl[2], font=fonts["3"], width=pl[9], color='rgb(94, 94, 94)')
        self.output_text(strings[3], pl[3], font=fonts["4"], width=pl[10], color='rgb(0, 0, 0)')

        self.output_text(strings[4], pl[4], font=fonts["5"], width=pl[11], color='rgb(23, 23, 189)')
        self.output_text(strings[5], pl[5], font=fonts["6"], width=pl[12], offsetx=45)
        if strings[6]!="":
            self.output_text(strings[6], pl[6], font=fonts["7"], width=pl[13], offsetx=45)

        # Save the file
        self.image.save("Final/"+self.imagename.replace("blank-", "")+"_%s.png" % language)
