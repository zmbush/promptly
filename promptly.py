#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import subprocess
import signal
from powerline import Powerlines
from powerline.line import Color


def getSubprocessOutput(arguments):
    s = subprocess.Popen(arguments, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    s.wait()
    if s.returncode == 0:
        return s.communicate()[0]
    else:
        raise subprocess.CalledProcessError('fail', 'fail')


def createTimeout(seconds):
    class TimeoutException(Exception):
        pass

    def timeout_function(f1):
        def f2(*args):
            def timeoutHandler(signum, frame):
                raise TimeoutException()
            old_handler = signal.signal(signal.SIGALRM, timeoutHandler)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                retval = f1(*args)
            except TimeoutException:
                retval = False
            finally:
                signal.signal(signal.SIGALRM, old_handler)
            signal.alarm(0)
            return retval
        return f2
    return timeout_function


def addSystemInfo(p):
    p.append('%c ', Color.CWD_FG, Color.CMD_PASSED_BG)


class Git(object):
    def __init__(self, p):
        self.p = p
        self._branch = None
        self._upstream = None

    def valid(self):
        try:
            s = subprocess.Popen(['git', 'rev-parse', '--git-dir'],
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            s.wait()
            if s.returncode == 0:
                return True
            else:
                return False
        except subprocess.CalledProcessError:
            return False

    def branch(self):
        if self._branch is None:
            branches = getSubprocessOutput(['git', 'branch']).split('\n')
            for b in branches:
                if b == '':
                    continue
                if b[0] == '*':
                    self._branch = b[2:]
        return self._branch

    def upstream(self):
        if self._upstream is None:
            branch = self.branch()
            if branch == '':
                return ''
            try:
                return getSubprocessOutput(['git', 'config', 'branch.' +
                                            branch + '.remote']).split('\n')[0]
            except:
                return '?'

    def colorOfStatus(self, stat):
        retval = (1, 0)
        swap = False
        check = ''
        if stat[0] == ' ':
            check = stat[1]
        elif stat[1] == ' ':
            check = stat[0]
            swap = True
        else:
            check = stat[:2]

        if 'M' == check:
            retval = Color.GIT_MOD_UNSTAGED_FG, Color.GIT_MOD_UNSTAGED_BG

        if swap:
            retval = (retval[1], retval[0])

        return retval

    def status(self):
        status = getSubprocessOutput(['git', 'status', '-s'])
        statuses = filter(bool, status.split('\n'))
        branch = self.branch()
        fgColor = Color.REPO_CLEAN_FG
        bgColor = Color.REPO_CLEAN_BG
        if len(statuses) > 0:
            fgColor = Color.REPO_DIRTY_FG
            bgColor = Color.REPO_DIRTY_BG
        self.p.append(u' \uE0A0 %s' % (branch,), fgColor, bgColor)
        if len(statuses) > 0:
            for status in statuses:
                self.p.newline()
                fgColor, bgColor = self.colorOfStatus(status[:2])
                self.p.append(' ' + status[:2].strip() + ' ', fgColor, bgColor)
                self.p.append(status[2:], Color.PATH_FG, Color.PATH_BG)

    def outgoing(self):
        pass

    def finish(self):
        pass

    def load(self):
        if self.valid() and '.git' not in os.getcwd():
            self.status()
            self.outgoing()
            self.finish()

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--cwd-only', action='store_true')
    arg_parser.add_argument('--mode', action='store', default='patched')
    arg_parser.add_argument('--shell', action='store', default='zsh')
    arg_parser.add_argument('prev_error', nargs='?', default=0, type=int)
    args = arg_parser.parse_args()

    p = Powerlines(mode=args.mode, shell=args.shell)
    addSystemInfo(p)
    g = Git(p)
    g.load()
    fgColor = Color.CMD_PASSED_FG
    bgColor = Color.CMD_PASSED_BG
    if args.prev_error != 0:
        fgColor = Color.CMD_FAILED_FG
        bgColor = Color.CMD_FAILED_BG
    p.append(' %# ', fgColor, bgColor)

    sys.stdout.write(p.draw() + ' ')
