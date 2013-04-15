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
    p.append('%c', Color.CWD_FG, Color.CMD_PASSED_BG)


class Git(object):
    def __init__(self, p):
        self.p = p

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

    def status(self):
        status = getSubprocessOutput(['git', 'status', '-s'])
        statuses = filter(bool, status.split('\n'))
        p.append
        if len(statuses) > 0:
            p.append("%d modified files" % len(statuses), Color.REPO_DIRTY_FG,
                     Color.REPO_DIRTY_BG)
        else:
            p.append("no changes", Color.REPO_CLEAN_FG, Color.REPO_CLEAN_BG)

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
    arg_parser.add_argument('prev_error', nargs='?', default=0)
    args = arg_parser.parse_args()

    p = Powerlines(mode=args.mode, shell=args.shell)
    addSystemInfo(p)
    g = Git(p)
    g.load()

    sys.stdout.write(p.draw())
