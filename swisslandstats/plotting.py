import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from rasterio.plot import show

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
Plots a land statistics %s with a categorical legend by means of
`rasterio.plot.show`

Parameters
----------%s
cmap : str or `~matplotlib.colors.Colormap`, optional
    A Colormap instance
legend : bool, optional
    If ``True``, display the legend
figsize: tuple of two ints, optional
    Size of the figure to create.
ax : axis object, optional
    Plot in given axis; if None creates a new figure
**show_kws : optional
    Keyword arguments to be passed to `rasterio.plot.show`

Returns
-------
ax : matplotlib axis
    axis with plot data
"""


def plot_ndarray(arr, transform=None, cmap=None, legend=False, figsize=None,
                 ax=None, **show_kws):
    if cmap is None:
        cmap = plt.get_cmap('terrain')

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')

    ax = show(arr, ax=ax, transform=transform, cmap=cmap, **show_kws)

    if legend:
        im = ax.get_images()[0]
        for class_val in np.unique(arr.ravel()):
            ax.plot(ax.get_xlim()[0],
                    ax.get_ylim()[0], 'o', c=cmap(im.norm(class_val)),
                    label=class_val)

        ax.legend()

    return ax


plot_ndarray.__doc__ = _plot_ndarray_doc % (
    'array',
    '\narr : array-like\n    data to display\ntransform : Affine, optional\n'
    '    The affine transform')
