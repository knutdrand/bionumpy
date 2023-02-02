import numpy as np
from numpy.testing import assert_equal
import pytest
from npstructures import npdataclass
from bionumpy.computation_graph import StreamNode
# from bionumpy.code_nodes import LeafNode, consume, NpDataclassStream


@npdataclass
class ExampleDatatype:
    a: int
    b: int
    c: int


@pytest.fixture
def data():
    return (np.array([0, 1, 2, 3, 4]), np.array([2, 3, 4, 1, 0]), np.array([100, 200, 1, 2, 3]))


@pytest.fixture
def stream_data(data):
    return tuple(StreamNode(iter([col[:2], col[2:4], col[4:]])) for col in data)


@pytest.fixture
def mixed_data(data, stream_data):
    return (stream_data[0], data[1], stream_data[2])


def add(a, b, c):
    return a+b


def two_step(a, b, c):
    return a*b+b-a


def complicated(a, b, c):
    d = a+b
    print(str(d))
    e = b * c
    print(str(e))
    f = c-a > 0
    print(str(f))
    g = np.where(f, np.exp(d+e+f), 1000)
    print(g)
    return(g)


@pytest.mark.parametrize("func", [add, two_step, complicated])
def test_equal(data, stream_data, func):
    true = func(*data)
    ours = func(*stream_data).compute()
    assert_equal(true, ours)


@pytest.mark.parametrize("func", [add, two_step, complicated])
@pytest.mark.skip('should fail')
def test_mixed_equal(data, mixed_data, func):
    true = func(*data)
    ours = func(*mixed_data).compute()
    assert_equal(true, ours)


def test_print(stream_data):
    a, b, c = stream_data
    print(a, b)
    print(complicated(a, b, c))


def test_reduce(stream_data, data):
    stream_data = stream_data[0]
    data = data[0]
    true = np.sum(data)
    s = np.sum(stream_data)
    print(s)
    solution = s.compute()
    print(true, solution)
    assert true == solution
