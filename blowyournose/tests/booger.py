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
    """A dummy object to create in tests, and check for proper cleanup.

    Create a Booger with a name and a scope.  The scope is "method" or "class",
    indicating whether the Booger should be cleaned up at the end of the method
    or the class.  The name is the name of a method or class.  Method-scoped
    objects can take class names.

    """

    # All the Boogers that have been created.
    all = []

    # A set of (scope, name) pairs that have been checked.
    all_checks = set()

    def __init__(self, name, scope='method'):
        self.name = name
        self.scope = scope

        caller_frame = inspect.stack()[1][0]
        self.location = "{}@{}".format(os.path.basename(caller_frame.f_code.co_filename), caller_frame.f_lineno)
        self.reported = False
        self.all.append(self)

    def __repr__(self):
        return "<Booger {!r} @0x{:x} from {}>".format(self.name, id(self), self.location)

    @classmethod
    def check_all(cls, scope, names):
        #print("*** {}".format(names), file=sys.stderr)
        gc.collect()

        cls.all_checks.update((scope, name) for name in names)

        # We expect three refs: 1) Booger.all, 2) the b local,
        # and 3) the argument to sys.getrefcount.
        OK_REF_COUNT = 3

        # The things we expect to be referring to boogers.
        us = [cls.all, inspect.currentframe()]

        for b in cls.all:
            if b.reported:
                continue
            if b.scope != scope:
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
    def check_all_checks(cls):
        """Check that every Booger name was checked for."""
        all_checked = set((b.scope, b.name) for b in cls.all)
        unchecked = all_checked - cls.all_checks
        if unchecked:
            print("** These Boogers were never checked:", file=sys.stderr)
            print("\n".join("{}: {}".format(*check) for check in unchecked), file=sys.stderr)


atexit.register(Booger.check_all_checks)

class BoogerCheck(Plugin):
    """
    A nose plugin only useful for testing BlowYourNose.  It checks the Boogers
    at the ends of method and class scopes.

    """

    score = 999

    def afterTest(self, test):
        # Called after test methods are run. Check for things that should have
        # been cleaned up by the end of the method.
        assert hasattr(test, 'byn_cleaned')
        Booger.check_all(scope='method', names=[test.test._testMethodName, test.test.__class__.__name__])

    def stopContext(self, context):
        # Called after classes and modules are done.  When we see a class,
        # check for the things that should have been cleaned up by the end of
        # the class.
        if inspect.isclass(context):
            Booger.check_all(scope='class', names=[context.__name__])
