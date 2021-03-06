#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Photobooth - a flexible photo booth software
# Copyright (C) 2018  Balthasar Reuter <photobooth at re - web dot eu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
import math
import random

from PIL import Image

from . import Camera


class CameraDummy(Camera):

    def __init__(self):

        super().__init__()

        self.hasPreview = True
        self.hasIdle = False

        random.seed()

        logging.info('Using CameraDummy')

    def getPreview(self):

        return self.getPicture()

    def getPicture(self):

        return plotColor(buildExpr(), buildExpr(), buildExpr())


# The following codes were taken from
# https://github.com/j2kun/random-art/blob/master/randomart.py to generate some
# psychedelic random pictures for testing purposes.

class X:

    def eval(self, x, y):

        return x


class Y:

    def eval(self, x, y):

        return y


class SinPi:

    def __init__(self, prob):

        self.arg = buildExpr(prob * prob)

    def eval(self, x, y):

        return math.sin(math.pi * self.arg.eval(x, y))


class CosPi:

    def __init__(self, prob):

        self.arg = buildExpr(prob * prob)

    def eval(self, x, y):

        return math.cos(math.pi * self.arg.eval(x, y))


class Times:

    def __init__(self, prob):

        self.lhs = buildExpr(prob * prob)
        self.rhs = buildExpr(prob * prob)

    def eval(self, x, y):

        return self.lhs.eval(x, y) * self.rhs.eval(x, y)


def buildExpr(prob=0.99):

    if random.random() < prob:
        return random.choice([SinPi, CosPi, Times])(prob)
    else:
        return random.choice([X, Y])()


def plotIntensity(exp, pixelsPerUnit=150):

    canvasWidth = 2 * pixelsPerUnit + 1
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    for py in range(canvasWidth):
        for px in range(canvasWidth):
            # Convert pixel location to [-1,1] coordinates
            x = float(px - pixelsPerUnit) / pixelsPerUnit
            y = -float(py - pixelsPerUnit) / pixelsPerUnit
            z = exp.eval(x, y)

            # Scale [-1,1] result to [0,255].
            intensity = int(z * 127.5 + 127.5)
            canvas.putpixel((px, py), intensity)

    return canvas


def plotColor(redExp, greenExp, blueExp, pixelsPerUnit=150):

    redPlane = plotIntensity(redExp, pixelsPerUnit)
    greenPlane = plotIntensity(greenExp, pixelsPerUnit)
    bluePlane = plotIntensity(blueExp, pixelsPerUnit)
    return Image.merge("RGB", (redPlane, greenPlane, bluePlane))
