from . import AlphabetEncoding
from .base_encoding import Encoding
from ..util import is_subclass_or_instance
import numpy as np


class KmerEncoding(Encoding):
    def __init__(self, alphabet_encoding: AlphabetEncoding, k: int):
        assert is_subclass_or_instance(alphabet_encoding, AlphabetEncoding), alphabet_encoding
        self._alphabet_encoding = alphabet_encoding
        self._k = k

    @property
    def k(self):
        return self._k

    def to_string(self, kmer):
        """
        Returns a human-readable string representation
        of an encoded kmer.
        """
        chars = (kmer >> (2 * np.arange(self._k))) & 3
        kmer = "".join(chr(b) for b in self._alphabet_encoding.decode(chars))
        return kmer

    def get_labels(self):
        assert self._k <= 5, "Only supported for k <= 5"
        return [self.to_string(kmer) for kmer in range(self._alphabet_encoding.alphabet_size**self._k)]

    def __str__(self):
        return f"{self._k}merEncoding({self._alphabet_encoding})"

    def __repr__(self):
        return f"KmerEncoding({self._alphabet_encoding}, {self._k})"

    def __eq__(self, other):
        if not isinstance(other, KmerEncoding):
            return False

        return self._k == other._k and self._alphabet_encoding == other._alphabet_encoding