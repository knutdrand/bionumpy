import numpy as np
from .genomic_data import GenomicArray, GenomicIntervals
from .computation_graph import Node
from .io.matrix_dump import Matrix

class Plotter:
    def __init__(self, plt):
        self.plt = plt
        self._show = False

    def set_config(self, **kwargs):
        accepted_configs = {'show'}
        for key, value in kwargs.items():
            assert key in accepted_configs
            if key == 'show':
                self._show =value

    def show(self, f=None):
        if not self._show:
            return
        if f is None:
            self.plt.show()
        else:
            f.show()

    def _conversion(self, data):
        if isinstance(data, GenomicIntervals):
            return data.get_pileup()
        return data

    def _plot_heatmap(self, matrix):

        fig, ax = self.plt.subplots()
        data = np.asanyarray(matrix.data)
        n_rows, n_cols = data.shape
        im = ax.imshow(data)
        
        # Show all ticks and label them with the respective list entries
        ax.set_xticks(np.arange(n_cols))
        ax.set_xticklabels(matrix.col_names)
        ax.set_yticks(np.arange(n_rows))
        ax.set_yticklabels(matrix.row_names)
        
        # Rotate the tick labels and set their alignment.
        self.plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        
        # Loop over data dimensions and create text annotations.
        if n_rows*n_cols<100:
            for i in range(n_rows):
                for j in range(n_cols):
                    text = ax.text(j, i, data[i, j],
                                   ha="center", va="center", color="w")
        fig.tight_layout()
        self.show()


    def _plot_list(self, data_list):
        data_list = [self._conversion(data) for data in data_list]
        if isinstance(data_list[0], GenomicArray):
            gc = data_list[0].genome_context
            assert all(isinstance(data, GenomicArray) for data in data_list)
            f, axes = self._subplots_for_genome(gc)
            # f, axes = self.plt.subplots(1, len(gc.chrom_sizes), sharey=True, sharex=True)
            for i, chromosome in enumerate(gc.chrom_sizes.keys()):
                for data in data_list:
                    axes[i].plot(np.asarray(data[chromosome]))
                axes[i].title.set_text(chromosome)
            self.show(f)
        else:
            raise NotImplementedError(f'{type(data)} not supported')        

    def _plot_dict(self, data_dict):
        data_dict = {key: self._conversion(data) for key, data in data_dict.items()}
        data = list(data_dict.values())[0]
        if isinstance(data, GenomicArray):
            gc = data.genome_context
            assert all(isinstance(data, GenomicArray) for data in data_dict.values())
            f, axes = self._subplots_for_genome(gc)
            for i, chromosome in enumerate(gc.chrom_sizes.keys()):
                for key, data in data_dict.items():
                    if i == 0:
                        label = key
                    else:
                        label = None
                    axes[i].plot(np.asarray(data[chromosome]), label=label)
                axes[i].title.set_text(chromosome)
            f.legend()
            self.show(f)
        else:
            raise NotImplementedError(f'{type(data)} not supported')        
        pass 

    def _subplots_for_genome(self, gc):
        return self.plt.subplots(len(gc.chrom_sizes), 1, sharey=True, sharex=True)
        
    def _plot_single(self, data):
        data = self._conversion(data)
        if isinstance(data, GenomicArray):
            f, axes = self._subplots_for_genome(data.genome_context)
            # f, axes = self.plt.subplots(1, len(data.genome_context.chrom_sizes), sharey=True, sharex=True)
            for i, chromosome in enumerate(data.genome_context.chrom_sizes.keys()):
                axes[i].plot(np.asarray(data[chromosome]))
                axes[i].title.set_text(chromosome)
            self.show(f)

        elif isinstance(data, Matrix):
            return self._plot_heatmap(data)
        else:
            raise NotImplementedError(f'{type(data)} not supported')

    def __call__(self, data):
        return self.plot(data)
    

    def plot(self, data):
        if isinstance(data, list):
            return self._plot_list(data)
        elif isinstance(data, dict):
            return self._plot_dict(data)
        return self._plot_single(data)


def convert_args_to_array(func):
    def convert(a):
        if isinstance(a, list):
            return [np.asarray(e) for e in a]
        elif isinstance(a, dict):
            return {key: np.asarray(val) for key, val in a.items()}
        else:
            return np.asarray(a)

    def new_func(*args, **kwargs):
        args = [convert(a) for a in args]
        kwargs = {key: convert(val) for key, val in kwargs.items()}
        return func(*args, **kwargs)
    return new_func


class PXWrapper:
    def __init__(self, px):
        self._px = px

    def __getattr__(self, name):
        func = getattr(self._px, name)
        return convert_args_to_array(func)

try:
    import plotly.express as _px
    px = PXWrapper(_px)
except:
    px = None
    
try:
    import matplotlib.pyplot as plt
    plt.style.use('Solarize_Light2')
    plot = Plotter(plt)
except:
    plot = None
