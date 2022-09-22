from itertools import tee
import numpy as np
from collections import defaultdict
import logging


def passthrough_print(stream, name):
    for elem in stream:
        # print(f"{name}: {elem}")
        yield elem



class GenWrap:
    def __init__(self, stream):
        self._stream = stream

    def __add__(self, other):
        if isinstance(other, BetterGenWrap):
            ret = self.__class__(None)
            ret.set_stream((a+b for a, b in zip(self.tee(ret, 0).iter(ret, 0), other.tee(ret, 1).iter(ret, 1))))
            return ret
        else:
            return self.__class__(e + other for e in self.tee())

    def __mul__(self, other):
        return self.__class__(a*b for a, b in zip(self.tee(), other.tee()))

    def tee(self):
        self._stream, new_stream = tee(self._stream)
        self._stream = passthrough_print(self._stream, "-")
        return new_stream

    def __iter__(self):
        return iter(self._stream)


class BetterGenWrap(GenWrap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._buffer = None

        if self._stream is not None:
            self.set_stream(self._stream)

        self._initial_askers = set()
        self._all_askers = set()
        self._remaining_askers = set()

    def set_stream(self, stream):
        self._stream = stream
        self._buffer = next(self._stream)
        assert self._buffer is not None

    def tee(self, asker, asker_id=0):
        asker = (asker, asker_id)
        if asker in self._initial_askers:
            logging.warning("The asker %s is already registered on this generator" % str(asker))
            return self

        self._initial_askers.add(asker)
        self._all_askers.add(asker)
        self._remaining_askers.add(asker)
        print("Added asker %s" % (str(asker)))
        return self

    def __str__(self):
        return "Stream %s" % (hash(self))

    def next(self, asker, asker_id=0):
        asker = (asker, asker_id)
        if asker not in self._all_askers:
            logging.error("Current asker: %s" % str(asker))
            logging.error("All askers: %s" % self._all_askers)
            raise Exception("Trying to iterate over %s from %s, but iteretor is exhausted" % (self, asker))

        if asker not in self._remaining_askers:
            # asker has come to next element
            self._buffer = next(self._stream)

            # remove all askers that did not iterate previous buffer
            self._all_askers -= self._remaining_askers

            # reset remaining askers
            self._remaining_askers = self._initial_askers.copy()

        self._remaining_askers.remove(asker)
        return self._buffer

    def iter(self, asker, asker_id=0):
        while True:
            try:
                yield self.next(asker, asker_id)
            except StopIteration:
                break

    def consume(self):
        return list(self.tee(self).iter(self))


def test2():

    a = BetterGenWrap((i for i in range(3)))
    b = BetterGenWrap((i for i in range(3)))
    c = a + b

    d = BetterGenWrap((10 for _ in range(3)))
    c = c + d

    result = c.consume()
    assert result == [10, 12, 14]
    print(result)


def test3():
    a = BetterGenWrap((i for i in range(3)))
    assert a.consume() == [0, 1, 2]
    assert a.consume() == []


def test4():
    a = BetterGenWrap((i for i in range(3)))
    b = a + a
    assert b.consume() == [0, 2, 4]


def test5():
    a = BetterGenWrap((i for i in range(5)))
    b = BetterGenWrap((i for i in range(5, 10)))
    c = BetterGenWrap((i for i in range(10, 15)))

    d = a + b + c + a + a + a
    e = d + a
    assert e.consume() == [15, 22, 29, 36, 43]


test5()


def test():
    a = BetterGenWrap((i for i in range(4)))
    b = BetterGenWrap((i for i in range(4)))

    c = a + b
    d = a + b

    e = c + d
    print(e.consume())



    lost = a + a
    print(lost._counter)

    for e in d.consume():
        print("RES: ", e)

    print(list(lost.consume()))

    print(lost._counter)
    #print(list(c))
    #d = c + b

    #print(list(d))







"""

ar, br, cr = (range(2, 22, 2), range(10), range(1, 11))

a = BetterGenWrap(passthrough_print(ar, "a"))
b = BetterGenWrap(passthrough_print(br, "b"))
c = BetterGenWrap(passthrough_print(cr, "c"))

tmp = a*c
tmp2 = b*a
print(tmp, tmp2)
res = tmp+b*a
print(res)
for r in res.consume():
    print(r)

a, b, c = (np.array(list(ar)), np.array(list(br)), np.array(list(cr)))

print(a*c+b*a)
"""