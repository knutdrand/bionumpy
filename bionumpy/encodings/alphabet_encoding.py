import numpy as np
from .base_encoding import Encoding


class AlphabetEncoding(Encoding):
    def __init__(self, alphabet: str):
        alphabet = [c.upper() for c in alphabet]
        self._alphabet = np.array([ord(c) for c in alphabet], dtype=np.uint8)
        lower_alphabet = (self._alphabet + ord("a")-ord("A"))
        self._alphabet = self._alphabet
        self._lookup = np.full(256, 255, dtype=np.uint8)
        self._lookup[self._alphabet] = np.arange(len(alphabet))
        self._lookup[lower_alphabet] = np.arange(len(alphabet))
        self._mask = np.zeros(256, dtype=bool)
        self._mask[self._alphabet] = True
        self._mask[lower_alphabet] = True

    def encode(self, byte_array):

        ret  = self._lookup[byte_array]
        # assert not np.any(ret==255), [chr(o) for o in (byte_array[ret==255])]
        return ret

    def decode(self, encoded):
        return self._alphabet[np.asarray(encoded)]

    @property
    def alphabet_size(self):
        return self._alphabet.size

    def get_alphabet(self):
        return [chr(c) for c in self._alphabet]

    def __str__(self):
        return f"""AlphabetEncoding('{"".join(self.get_alphabet())}')"""

    def __eq__(self, other):
        if not isinstance(other, AlphabetEncoding):
            return False
        return np.all(self._alphabet == other._alphabet)


ACTGEncoding = AlphabetEncoding("ACTG")
ACGTEncoding = AlphabetEncoding("ACGT")
ACTGnEncoding = AlphabetEncoding("ACTGn")
DigitEncoding = AlphabetEncoding("0123456789")
DNAEncoding = ACGTEncoding
ACUGEncoding = AlphabetEncoding("ACUG")
RNAENcoding = ACUGEncoding
AminoAcidEncoding = AlphabetEncoding('ACDEFGHIKLMNPQRSTVWY')
BamEncoding = AlphabetEncoding("=ACMGRSVTWYHKDBN")
CigarOpEncoding = AlphabetEncoding("MIDNSHP=X")
