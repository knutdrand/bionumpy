import numpy as np
from .sequences import Sequence, as_encoded_sequence_array
from npstructures import RaggedArray

from abc import abstractmethod


class RollableFunction:
    @abstractmethod
    def __call__(self, sequence: Sequence):
        """Function that returns a single value

        Broadcastable function that maps a sequence to a single value.


        Parameters
        ----------
        sequence : Sequence
            A sequence (or set of sequences) of length given by `self.window_size`

        Examples
        --------
        4

        """
        return NotImplemented

    def rolling_window(self, _sequence: RaggedArray, window_size: int = None, mode="valid"):
        """Applies the function `self.__call__` to all subsequences in _sequence

        Uses sliding_window_view to apply `self.__call__` to all subsequences of length
        `self.window_size` or `window_size` in `_sequence`


        Parameters
        ----------
        _sequence : RaggedArray
            Sequence or set of RaggedArray to apply the rolling window to
        window_size : int
            The size of the rolling window (should ideally be set by `self.window_size`)
        mode : ["valid", "same", "full"]
            shape of output
        """
        if window_size is None:
            window_size = self.window_size
        if not isinstance(_sequence, np.ndarray):
            if hasattr(self, "_encoding") and self._encoding is not None:
                _sequence = as_encoded_sequence_array(_sequence, encoding=self._encoding)
            elif not isinstance(_sequence, RaggedArray):
                _sequence = RaggedArray(_sequence)

        shape, sequence = (_sequence.shape, _sequence.ravel())
        if mode == "valid":
            windows = np.lib.stride_tricks.sliding_window_view(sequence, window_size, subok=True)
        elif mode == "same":
            windows = np.lib.stride_tricks.as_strided(sequence, strides=sequence.strides + sequence.strides, shape=sequence.shape + (window_size,),
                                                      writeable=False)
        convoluted = self(windows)
        if isinstance(_sequence, RaggedArray):
            out = RaggedArray(convoluted, shape)
        elif isinstance(_sequence, np.ndarray):
            out = np.lib.stride_tricks.as_strided(convoluted, shape)
        if mode == "valid":
            return out[..., : (-window_size + 1)]
        elif mode == "same":
            out[..., (-window_size + 1):] = 0
            return out
