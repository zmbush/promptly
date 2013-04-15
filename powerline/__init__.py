#!/usr/bin/env python
# -*- coding: utf-8 -*-
from powerline import line


class Powerline(object):
    def __init__(self, mode, shell):
        self.line = line.Line(mode, shell)

    def append(self, content, fg, bg, separator=None, separator_fg=None):
        self.line.append(line.Segment(self.line, content, fg, bg,
                                      separator, separator_fg))

    def draw(self):
        self.line.draw()
