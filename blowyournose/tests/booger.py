from __future__ import print_function

import gc
import inspect
import os.path
import pprint
import sys

from nose.plugins import Plugin
import objgraph


class Booger(object):
    all = []

    def __init__(self, name='Unknown'):
        self.name = name
        caller_frame = inspect.stack()[1][0]
        self.location = "{}@{}".format(os.path.basename(caller_frame.f_code.co_filename), caller_frame.f_lineno)
        self.reported = False
        self.all.append(self)

    def __repr__(self):
        return "<Booger {!r} @0x{:x} from {}>".format(self.name, id(self), self.location)

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
                print("** {!r} unpicked, with these referrers:".format(b), file=sys.stderr)
                pprint.pprint(referrers, stream=sys.stderr)
                objgraph.show_backrefs(
                    [b],
                    filename="booger_{0:x}.png".format(id(b)),
                    extra_ignore=map(id, us),
                    max_depth=6,
                )
                b.reported = True


class BoogerCheck(Plugin):

    score = 999

    def afterTest(self, test):
        assert hasattr(test, 'byn_cleaned')
        Booger.check_all()
