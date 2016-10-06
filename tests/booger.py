import atexit
import gc
import pprint
import sys


class Booger(object):
    all = []

    def __init__(self):
        self.all.append(self)

    def __repr__(self):
        return "<Booger>"

    @classmethod
    def check_all(cls):
        gc.collect()
        # Three refs: Booger.all, the b local, and the argument to
        # sys.getrefcount.
        OK_REF_COUNT = 3
        for b in cls.all:
            if sys.getrefcount(b) > OK_REF_COUNT:
                print(b)
                pprint.pprint(gc.get_referrers(b))

atexit.register(Booger.check_all)
