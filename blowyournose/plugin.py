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
        while method is not None:
            if hasattr(method, "patchings"):
                if hasattr(method, "im_func"):
                    method.im_func.patchings = None
                else:
                    method.patchings = None

            # Is this a decorated method?
            method = getattr(method, "__wrapped__", None)

        test.byn_cleaned = True
