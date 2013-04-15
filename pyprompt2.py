#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Color:
    # The following link is a pretty good resources for color values:
    # http://www.calmar.ws/vim/color-output.png

    PATH_BG = 237  # dark grey
    PATH_FG = 250  # light grey
    CWD_FG = 254  # nearly-white grey
    SEPARATOR_FG = 244

    REPO_CLEAN_BG = 148  # a light green color
    REPO_CLEAN_FG = 0  # black
    REPO_DIRTY_BG = 161  # pink/red
    REPO_DIRTY_FG = 15  # white

    CMD_PASSED_BG = 236
    CMD_PASSED_FG = 15
    CMD_FAILED_BG = 161
    CMD_FAILED_FG = 15

    SVN_CHANGES_BG = 148
    SVN_CHANGES_FG = 22  # dark green

    VIRTUAL_ENV_BG = 35  # a mid-tone green
    VIRTUAL_ENV_FG = 00


class Powerline:
    symbols = {
        'compatible': {
            'separator': u'\u25B6',
            'separator_thin': u'\u276F'
        },
        'patched': {
            'separator': u'\u2B80',
            'separator_thin': u'\u2B81'
        },
        'flat': {
            'separator': '',
            'separator_thin': ''
        },
    }

    color_templates = {
        'bash': '\\[\\e%s\\]',
        'zsh': '%%{%s%%}',
        'bare': '%s',
    }

    root_indicators = {
        'bash': ' \\$ ',
        'zsh': ' \\$ ',
        'bare': ' $ ',
    }

    user_prompt = {
        'bash': ' \\u',
        'zsh': ' %n'
    }

    host_prompt = {
        'bash': ' \\h',
        'zsh': ' %m'
    }

    def __init__(self, mode, shell):
        self.shell = shell
        self.color_template = self.color_templates[shell]
        self.root_indicator = self.root_indicators[shell]
        self.reset = self.color_template % '[0m'
        self.separator = Powerline.symbols[mode]['separator']
        self.separator_thin = Powerline.symbols[mode]['separator_thin']
        self.segments = []

    def color(self, prefix, code):
        return self.color_template % ('[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def append(self, segment):
        self.segments.append(segment)

    def draw(self):
        shifted = self.segments[1:] + [None]
        return (''.join((c.draw(n) for c, n in zip(self.segments, shifted)))
                + self.reset).encode('utf-8')


class Segment:
    def __init__(self, powerline, content, fg, bg, separator=None,
            separator_fg=None):
        self.powerline = powerline
        self.content = content
        self.fg = fg
        self.bg = bg
        self.separator = separator or powerline.separator
        self.separator_fg = separator_fg or bg

    def draw(self, next_segment=None):
        if next_segment:
            separator_bg = self.powerline.bgcolor(next_segment.bg)
        else:
            separator_bg = self.powerline.reset

        return ''.join((
            self.powerline.fgcolor(self.fg),
            self.powerline.bgcolor(self.bg),
            self.content,
            separator_bg,
            self.powerline.fgcolor(self.separator_fg),
            self.separator))
