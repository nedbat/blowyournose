from nose.plugins import Plugin

class BlowYourNose(Plugin):

    # `test` is a Nose test object. `test.test` is the actual TestCase object
    # being run.

    def beforeTest(self, test):
        test.byn_attrs = set(dir(test.test))

    def afterTest(self, test):
        obj = test.test
        for attr in dir(obj):
            if attr not in test.byn_attrs:
                delattr(obj, attr)
