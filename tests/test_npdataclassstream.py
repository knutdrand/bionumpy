import pytest
from bionumpy.npdataclassstream import  NpDataclassStream, NpDataClassFieldStream
from npstructures.npdataclasses import npdataclass
import numpy as np

@npdataclass
class DummyClass:
    data1: np.ndarray
    data2: np.ndarray


@pytest.fixture
def stream():
    return NpDataclassStream(
        (DummyClass(np.arange(5), 2 * np.arange(5)) for _ in range(3)),
        buffer_type=None
    )

@pytest.fixture
def field_stream():
    return NpDataClassFieldStream(
        (np.arange(5) for _ in range(3))
    )


def test_field_stream_add(field_stream):
    field_stream = field_stream + 1
    for e in field_stream:
        assert np.all(e == np.arange(5)+1)


def test_field_stream_dual_generators(field_stream):
    mask1 = field_stream > 2
    mask2 = field_stream == 3

    print(list(mask1))
    print(list(mask2))


def test_stream_broadcasting(stream):

    mask1 = stream.data1 > 2
    mask2 = stream.data2 < 4

    print(next(mask1))
    print(type(mask2))
