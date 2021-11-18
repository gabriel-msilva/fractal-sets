from typing import Union
import warnings

import numpy as np
from numba import jit, prange
import matplotlib.pyplot as plt


def _set_limits(center, zoom):
    delta = (1.5 + 1.5j) / zoom
    lims = [center - delta, center + delta]
    
    return np.real(lims), np.imag(lims)


def _create_grid(xlim, ylim, number_points):
    x, y = np.ogrid[xlim[0]:xlim[1]:int(number_points) * 1j, 
                    ylim[0]:ylim[1]:int(number_points) * 1j]
    
    return (x + y * 1j).T


@jit(nopython=True, parallel=True)
def _logistic_map(z, c, count, max_iter):
    px, py = z.shape
    
    for i in prange(px):
        for j in prange(py):
            while (np.abs(z[i, j]) <= 1e8) and (count[i, j] < max_iter):
                z[i, j] = z[i, j]**2 + c[i, j]
                count[i, j] += 1


def _apply_smoothing(count, z, max_iter):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        count = np.where(count < max_iter,
                         count + 1 - np.log2(np.log2(np.abs(z))),
                         count)
    
    return count

def _plot_set(count, xlim, ylim, ax, axis_labels, **kwargs):
    if ax:
        ax.imshow(count, extent=[*xlim, *ylim], origin='lower', **kwargs)
        
        return ax
    
    fig = plt.figure()
    plt.imshow(count, extent=[*xlim, *ylim], origin='lower', **kwargs)
    
    plt.axis(axis_labels)
    
    return fig


def plot_mandelbrot(
        max_iter: int=200,
        center: complex=-0.5,
        zoom: int=1,
        number_points: int=300,
        ax: plt.axis=None,
        axis_labels: bool=False,
        smoothing: bool=False,
        **kwargs
        ) -> Union[plt.Figure, plt.Axes]:
    """
    Plot the Mandelbrot set with number of iterations mapped to color.

    Parameters
    ----------
    max_iter : int, default 200
        Maximum number of iterations.
    center : complex, default -0.5
        Center point of the plot.
    zoom : int, default 1
        Zoom ratio.
    number_points : int, default 300
        Number of `c` points between the axis limits.
    ax : matplotlib.axes._axes.Axes, optional
        If not None, draw plot to `ax`. Otherwise, return a new figure.
    axis_labels : bool, default False
        If True, display axis lines and labels.
    smoothing : bool, default False
        If True, apply continuous color smoothing.
    **kwargs
        Keyword arguments passed to ``matplotlib.pyplot.imgshow()``.

    Returns
    -------
    matplotlib.figure.Figure or matplotlib.axes._axes.Axes
        Mandelbrot set plot
    """
    max_iter = int(max_iter)
    
    xlim, ylim = _set_limits(center, zoom)
    c = _create_grid(xlim, ylim, number_points)
    
    z = np.zeros(c.shape, dtype=complex)
    count = np.zeros(c.shape, dtype=float)
    
    _logistic_map(z, c, count, max_iter)
    
    if smoothing:
        count = _apply_smoothing(count, z, max_iter)
    
    return _plot_set(count, xlim, ylim, ax, axis_labels, **kwargs)


def plot_julia(
        c: complex,
        center: complex=0,
        max_iter: int=200,
        zoom: float=1,
        number_points: int=300,
        ax=None,
        axis_labels='off',
        smoothing=False,
        **kwargs
        ) -> Union[plt.Figure, plt.Axes]:
    """
    Plot the Julia set with number of iterations mapped to color.

    Parameters
    ----------
    c : complex
        Constant complex number of the logistic map, :math:`z_{n+1} = z_n^2 + c`.
    center : complex, default -0.5
        Center point of the plot.
    zoom : int, default 1
        Zoom ratio.
    max_iter : int, default 200
        Maximum number of iterations.
    number_points : int, default 300
        Number of `c` points between the axis limits.
    ax : matplotlib.axes._axes.Axes, optional
        If not None, draw plot to `ax`. Otherwise, return a new figure.
    axis_labels : bool, default False
        If True, display axis lines and labels.
    smoothing : bool, default False
        If True, apply continuous color smoothing.
    **kwargs
        Keyword arguments passed to ``matplotlib.pyplot.imgshow()``.

    Returns
    -------
    matplotlib.figure.Figure or matplotlib.axes._axes.Axes
        Julia set plot
    """
    xlim, ylim = _set_limits(center=center, zoom=zoom)
    z = _create_grid(xlim, ylim, number_points)
    
    c = np.full(z.shape, c, dtype=complex)
    count = np.zeros(z.shape, dtype=float)
    
    _logistic_map(z, c, count, int(max_iter))
    
    if smoothing:
        count = _apply_smoothing(count, z, max_iter)

    return _plot_set(count, xlim, ylim, ax, axis_labels, **kwargs)
