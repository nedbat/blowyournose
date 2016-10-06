from __future__ import print_function

import atexit
import gc
import inspect
import os.path
import pprint
import sys

from nose.plugins import Plugin
import objgraph


class Booger(object):
    all = []

    all_check_names = set()

    def __init__(self, name='Unknown', when='method'):
        self.name = name
        self.when = when

        caller_frame = inspect.stack()[1][0]
        self.location = "{}@{}".format(os.path.basename(caller_frame.f_code.co_filename), caller_frame.f_lineno)
        self.reported = False
        self.all.append(self)

    def __repr__(self):
        return "<Booger {!r} @0x{:x} from {}>".format(self.name, id(self), self.location)

    @classmethod
    def check_all(cls, when, names):
        gc.collect()

        cls.all_check_names.update(names)

        # We expect three refs: 1) Booger.all, 2) the b local,
        # and 3) the argument to sys.getrefcount.
        OK_REF_COUNT = 3

        # The things we expect to be referring to boogers.
        us = [cls.all, inspect.currentframe()]

        for b in cls.all:
            if b.reported:
                continue
            if b.when != when:
                continue
            if b.name not in names:
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

    @classmethod
    def check_all_names(cls):
        """Check that every Booger name was checked for."""
        all_names = set(b.name for b in cls.all)
        unchecked = all_names - cls.all_check_names
        if unchecked:
            print("** These Boogers were never checked:", file=sys.stderr)
            print("\n".join(unchecked), file=sys.stderr)


atexit.register(Booger.check_all_names)

class BoogerCheck(Plugin):

    score = 999

    def afterTest(self, test):
        assert hasattr(test, 'byn_cleaned')
        Booger.check_all(when='method', names=['fooey'])
