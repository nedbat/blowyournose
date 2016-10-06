from __future__ import print_function

import atexit
import gc
import pprint
import sys

from nose.plugins import Plugin


class Booger(object):
    all = []

    def __init__(self):
        self.all.append(self)

    def __repr__(self):
        return "<Booger>"

    @classmethod
    def check_all(cls):
        gc.collect()

        # We expect three refs: 1) Booger.all, 2) the b local,
        # and 3) the argument to sys.getrefcount.
        OK_REF_COUNT = 3

        for b in cls.all:
            if sys.getrefcount(b) > OK_REF_COUNT:
                print(b, file=sys.stderr)
                pprint.pprint(gc.get_referrers(b), stream=sys.stderr)


class BoogerCheck(Plugin):

    score = 999

    def afterTest(self, test):
        assert hasattr(test, 'byn_cleaned')
        Booger.check_all()
