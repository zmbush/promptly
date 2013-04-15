#!/usr/bin/env python
# -*- coding: utf-8 -*-

from powerline.line import Line, Segment


class Powerline(object):
    def __init__(self, mode, shell):
        self.line = Line(mode, shell)

    def append(self, content, fg, bg, separator=None, separator_fg=None):
        self.line.append(Segment(self.line, content, fg, bg, separator,
                                 separator_fg))

    def draw(self):
        self.line.draw()
