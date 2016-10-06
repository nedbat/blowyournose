from __future__ import print_function

import atexit
import gc
import inspect
import pprint
import sys

from nose.plugins import Plugin


class Booger(object):
    all = []

    def __init__(self):
        self.all.append(self)
        self.reported = False

    def __repr__(self):
        return "<Booger>"

    @classmethod
    def check_all(cls):
        gc.collect()

        # We expect three refs: 1) Booger.all, 2) the b local,
        # and 3) the argument to sys.getrefcount.
        OK_REF_COUNT = 3

        # The things we expect to be referring to boogers.
        us = [cls.all, inspect.currentframe()]

        for b in cls.all:
            if b.reported:
                continue
            if sys.getrefcount(b) > OK_REF_COUNT:
                # Show the unexpected referrers.
                referrers = [r for r in gc.get_referrers(b) if r not in us]
                print("** Unpicked booger with these referrers:", file=sys.stderr)
                pprint.pprint(referrers, stream=sys.stderr)
                b.reported = True


class BoogerCheck(Plugin):

    score = 999

    def afterTest(self, test):
        assert hasattr(test, 'byn_cleaned')
        Booger.check_all()
