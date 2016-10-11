from __future__ import print_function

import sys
import inspect

from nose.plugins import Plugin

DDT_ATTR = '%values'


class BlowYourNose(Plugin):

    score = 1000

    # `test` is a Nose test object. `test.test` is the actual TestCase object
    # being run.

    def beforeTest(self, test):
        # Record the pre-existing attributes.
        test.byn_attrs = set(getattr(test.test, '__dict__', {}))

    def afterTest(self, test):
        obj = test.test

        # Delete any attribute that we didn't have at the beginning.
        for attr in getattr(obj, '__dict__', {}).keys():
            if attr not in test.byn_attrs:
                delattr(obj, attr)

        # Is there a mock.patch on the test method?
        method = getattr(obj, obj._testMethodName)
        if hasattr(method, DDT_ATTR):
            context = test.context
            if not hasattr(context, "blowyournose_ddt_methods"):
                context.blowyournose_ddt_methods = []
            context.blowyournose_ddt_methods.append(method)
        else:
            self.clean_method(method)

        test.byn_cleaned = True

    def clean_method(self, method):
        while method is not None:
            if hasattr(method, "patchings"):
                if hasattr(method, "im_func"):
                    method.im_func.patchings = None
                else:
                    method.patchings = None

            # Is this a decorated method?
            method = getattr(method, "__wrapped__", None)

    def startContext(self, context):
        if inspect.isclass(context):
            context.byn_attrs = set(getattr(context, '__dict__', {}))

    def stopContext(self, context):
        for method in getattr(context, "blowyournose_ddt_methods", ()):
            self.clean_method(method)

        # N.B. This must go after the blowyournose_ddt_methods attr
        # has already been used for cleanup
        if inspect.isclass(context):
            # Delete any attribute that we didn't have at the beginning.
            for attr in getattr(context, '__dict__', {}).keys():
                if attr not in context.byn_attrs and attr != 'byn_attrs':
                    delattr(context, attr)
            del context.byn_attrs
