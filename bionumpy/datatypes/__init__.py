from ..typing import SequenceID
import numpy as np
from typing import List, Union
from ..encodings import (CigarOpEncoding, BamEncoding, QualityEncoding,
                         CigarEncoding, StrandEncoding)
from ..encodings.vcf_encoding import PhasedGenotypeRowEncoding, GenotypeRowEncoding, PhasedHaplotypeRowEncoding
from ..bnpdataclass import bnpdataclass, BNPDataClass
from .gtf import GFFEntry, GFFExonEntry, GFFGeneEntry, GFFTranscriptEntry, GTFEntry
SequenceID = str

@bnpdataclass
class LocationEntry:
    chromosome: str
    position: int


@bnpdataclass
class StrandedLocationEntry(LocationEntry):
    strand: StrandEncoding


@bnpdataclass
class BedGraph:
    chromosome: str
    start: int
    stop: int
    value: float


@bnpdataclass
class RawSeqeuence:
    sequence: str


@bnpdataclass
class SequenceEntry:
    name: SequenceID
    sequence: str


@bnpdataclass
class SequenceEntryWithQuality:
    name: str
    sequence: str
    quality: QualityEncoding


@bnpdataclass
class Interval:
    chromosome: SequenceID
    start: int
    stop: int


@bnpdataclass
class StrandedInterval(Interval):
    strand: StrandEncoding


@bnpdataclass
class Bed6(Interval):
    name: str
    score: int
    strand: StrandEncoding


@bnpdataclass
class NarrowPeak(Bed6):
    signal_value: float
    p_value: float
    q_value: float
    summit: int


@bnpdataclass
class Bed12(Bed6):
    thick_start: int
    thick_end: int
    item_rgb: str
    block_count: int
    block_sizes: List[int]
    block_starts: List[int]


@bnpdataclass
class Variant:
    chromosome: str
    position: int
    ref_seq: str
    alt_seq: str

    def is_snp(self):
        return (self.ref_seq.lengths == 1) & (self.alt_seq.lengths == 1)


@bnpdataclass
class VCFEntry:
    chromosome: str
    position: int
    id: str
    ref_seq: str
    alt_seq: str
    quality: str
    filter: str
    info: Union[BNPDataClass, str]
    # genotypes: str

    def is_snp(self):
        return (self.ref_seq.lengths == 1) & (self.alt_seq.lengths == 1)

@bnpdataclass
class VCFEntryWithGenotypes(VCFEntry):
    genotype: str

@bnpdataclass
class VCFGenotypeEntry(VCFEntry):
    genotypes: GenotypeRowEncoding


@bnpdataclass
class PhasedVCFGenotypeEntry(VCFEntry):
    genotypes: PhasedGenotypeRowEncoding


@bnpdataclass
class PhasedVCFHaplotypeEntry(VCFEntry):
    genotypes: PhasedHaplotypeRowEncoding


class SNP(Variant):
    pass


class SortedIntervals:
    def __init__(self, data):
        self.data = np.asanyarray(data)
        assert data.shape[-1] == 2
        assert len(data.shape) == 2

        self.starts = self.data[..., 0]
        self.ends = self.data[..., 1]

    def in_intervals(self, position):
        idx = np.minimum(
            np.searchsorted(self.starts, position, side="left"), self.starts.size - 1
        )
        return (position >= self.starts[idx]) & (position < self.ends[idx])

    @classmethod
    def concatenate(cls, elements):
        return cls(np.vstack([element.data for element in elements]))


@bnpdataclass
class SAMEntry:
    name: str
    flag: int
    chromosome: str
    position: int
    mapq: int
    cigar: str
    next_chromosome: str
    next_position: int
    length: int
    sequence: str
    quality: str
    extra: str

@bnpdataclass
class BamEntry:
    chromosome: str
    name: str
    flag: int
    position: int
    mapq: int
    cigar_op: CigarOpEncoding
    cigar_length: CigarEncoding
    sequence: BamEncoding
    quality: QualityEncoding


@bnpdataclass
class ChromosomeSize:
    name: str
    size: int


@bnpdataclass
class GfaPath:
    name: str
    node_ids: List[int]
    directions: List[int]
