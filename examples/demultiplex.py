from bionumpy.rollable import RollableFunction
from bionumpy.sequences import as_sequence_array

import numpy as np
import bionumpy as bionp

class MatchSequence(RollableFunction):
    def __init__(self, matching_sequence):
        self._matching_sequence = as_sequence_array(matching_sequence)
        self.window_size = len(matching_sequence)

    def __call__(self, sequence):
        return np.all(sequence == self._matching_sequence, axis=-1)

matcher = MatchSequence("CG")

#with bionp.open('example_1_R1_001.fastq') as source_R1:
source_R1 = bionp.open('example_1_R1_001.fastq')

outfile = bionp.open('out.fastq', mode='w')
for chunk in source_R1:
    print(chunk.sequence)
    print(matcher.rolling_window(chunk.sequence))

    # outfile.write(mt)

outfile.close()
source_R1.close()

print(extract)

