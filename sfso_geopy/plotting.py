import matplotlib.pyplot as plt
import numpy as np

from matplotlib import colors

__all__ = ['noas04_4_cmap']

_nodata_c = (1, 1, 1, 0)  # transparent white
_noas04_4_cdict = {  # based on Corine's land cover nomenclature Level 1
    1: (0.9019607843137255, 0, 0.30196078431372547, 1),
    2: (1, 1, 0.6588235294117647, 1),
    3: (0.5019607843137255, 1, 0, 1),
    4: (0, 0.8, 0.9490196078431372, 1)
}

noas04_4_cmap = colors.ListedColormap([
    _noas04_4_cdict[key] if key in _noas04_4_cdict else _nodata_c
    for key in range(5)
], name='noas04_4', N=5)


def plot_ndarray(arr, cmap=None, ax=None, legend=False, figsize=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')

    ax.imshow(arr, cmap=cmap)

    if legend:
        classes = np.unique(arr.ravel())

        for cl in classes:
            ax.plot(0, 0, '-', c=noas04_4_cmap(cl), label=cl)

        ax.legend()

    return ax
