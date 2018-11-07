import matplotlib.pyplot as plt
import numpy as np

from matplotlib import colors

__all__ = ['noas04_4_cmap', 'plot_ndarray']

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

_plot_ndarray_doc = """
Plot an array

Parameters
----------%s
cmap : str or `~matplotlib.colors.Colormap`, optional
    A Colormap instance
ax : axis object, optional
    Plot in given axis; if None creates a new figure
legend : bool, optional
    If ``True``, display the legend
figsize: tuple of two ints, optional
    Size of the figure to create.

Returns
-------
ax : matplotlib axis
    axis with plot data
"""


def plot_ndarray(arr, cmap=None, ax=None, legend=False, figsize=None):
    if cmap is None:
        cmap = plt.get_cmap('terrain')

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')

    im = ax.imshow(arr, cmap=cmap)

    if legend:
        for class_val in np.unique(arr.ravel()):
            ax.plot(0, 0, 'o', c=cmap(im.norm(class_val)), label=class_val)

        ax.legend()

    return ax


plot_ndarray.__doc__ = _plot_ndarray_doc % \
    '\narr : array-like\n    data to display'
