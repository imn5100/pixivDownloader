# -*- coding: utf-8 -*-
import threading


class AtomicInteger(object):
    def __init__(self, val=0):
        self.lock = threading.Lock()
        self.val = val

    def get(self):
        return self.val

    def getAndSet(self, val):
        self.lock.acquire()
        current_val = self.val
        self.val = val
        self.lock.release()
        return current_val

    def getAndInc(self):
        return self.getAndAdd(1)

    def getAndDec(self):
        return self.getAndAdd(-1)

    def getAndAdd(self, delta):
        self.lock.acquire()
        current_val = self.val
        self.val += delta
        self.lock.release()
        return current_val

    def __str__(self):
        return str(self.val)

    def __cmp__(self, other):
        AtomicInteger.assert_int(other)
        return self.get() - other

    @staticmethod
    def assert_int(other):
        assert type(other) == int
