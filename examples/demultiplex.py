import  bionumpy.rollable as rlb
from bionumpy.sequences import as_sequence_array
from importlib import reload
import numpy as np
import bionumpy as bionp
reload(rlb)

class MatchSequence(rlb.RollableFunction):
    def __init__(self, matching_sequence):
        self._matching_sequence = as_sequence_array(matching_sequence)
        self.window_size = len(matching_sequence)

    def __call__(self, sequence):
        print(sequence.shape, self._matching_sequence.shape, type(self._matching_sequence))
        # print(sequence == self._matching_sequence)
        return np.all(sequence == self._matching_sequence, axis=-1)

matcher = MatchSequence("CG")

#with bionp.open('example_1_R1_001.fastq') as source_R1:
source_R1 = bionp.open("/home/knut/Data/reads/ENCFF046ZGZ.fastq.gz")

outfile = bionp.open('out.fastq', mode='w')
for chunk in source_R1:
    print(len(chunk))
    print(chunk.sequence.shape, chunk.sequence.size, len(chunk.sequence))
    matches = matcher.rolling_window(chunk.sequence)
    seq_matches = matches.any(axis=-1)
    filtered = chunk[seq_matches]
    print(len(filtered))
    outfile.write(chunk[seq_matches])

#outfile.close()
#source_R1.close()

#print(extract)

