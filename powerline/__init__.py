#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from powerline import line


class Powerlines(object):
    def __init__(self, mode, shell):
        self.mode = mode
        self.shell = shell
        self.lines = []
        self.lines.append(line.Line(self.mode, self.shell))

    def newline(self):
        self.lines.append(line.Line(self.mode, self.shell))

    def append(self, content, fg, bg, separator=None, separator_fg=None):
        self.lines[-1].append(line.Segment(self.lines[-1], content, fg, bg,
                                           separator, separator_fg))

    def draw(self):
        return u'\n'.join(line.draw() for line in self.lines).encode('utf-8')
