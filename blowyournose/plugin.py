from __future__ import print_function

import sys

from nose.plugins import Plugin

class BlowYourNose(Plugin):

    score = 1000

    # `test` is a Nose test object. `test.test` is the actual TestCase object
    # being run.

    def beforeTest(self, test):
        # Record the pre-existing attributes.
        test.byn_attrs = set(dir(test.test))

    def afterTest(self, test):
        obj = test.test

        # Delete any attribute that we didn't have at the beginning.
        for attr in dir(obj):
            if attr not in test.byn_attrs:
                delattr(obj, attr)

        # Is there a mock.patch on the test method?
        method = getattr(obj, obj._testMethodName)
        if hasattr(method, "patchings"):
            method.im_func.patchings = None

        # Is this a decorated method?
        if hasattr(method, '__wrapped__'):
            print("---", method, file=sys.stderr)
            print(dir(method), file=sys.stderr)
            print("patchings =", getattr(method, "patchings", 'xxx'), file=sys.stderr)
            # Drop the patchings from the wrapped function.
            wrapped = getattr(method, "__wrapped__", None)
            if wrapped:
                print("-----", wrapped, file=sys.stderr)
                print(dir(wrapped), file=sys.stderr)
                print("__dict__ =", wrapped.__dict__, file=sys.stderr)
                if hasattr(wrapped, "patchings"):
                    wrapped.patchings = None

        test.byn_cleaned = True
