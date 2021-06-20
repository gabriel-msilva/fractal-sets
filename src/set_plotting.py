import numpy as np
from numba import jit
import matplotlib.pyplot as plt


def plot_mendelbrot(
        max_iter: int=200,
        center: complex=-0.5,
        zoom: int=1,
        number_points: int=300,
        cmap='gist_heat',
        axis_labels='off',
        **kwargs
        ):
    xlim, ylim = _set_limits(center, zoom)
    c = _create_grid(xlim, ylim, number_points)
    
    z = np.zeros(c.shape, dtype=complex)
    count = np.zeros(c.shape, dtype=int)
    
    z, count = _logistic_map(z, c, count, int(max_iter))
    
    return _plot_set(count, xlim, ylim, cmap, axis_labels, **kwargs)


def plot_julia(
        c: complex,
        max_iter: int=200,
        number_points: int=300,
        cmap='gist_heat', 
        axis_labels='off',
        **kwargs
        ):
    xlim, ylim = _set_limits(center=0, zoom=1)
    z = _create_grid(xlim, ylim, number_points)
    
    count = np.zeros(z.shape, dtype=int)
    
    z, count = _logistic_map(z, c, count, int(max_iter))
    
    return _plot_set(count, xlim, ylim, cmap, axis_labels, **kwargs)


def _set_limits(center, zoom):
    delta = (1.5 + 1.5j) / zoom
    lims = [center - delta, center + delta]
    
    return np.real(lims), np.imag(lims)


def _create_grid(xlim, ylim, number_points):
    x, y = np.ogrid[xlim[0]:xlim[1]:int(number_points) * 1j, 
                    ylim[0]:ylim[1]:int(number_points) * 1j]
    
    return (x + y * 1j).T


@jit(nopython=True)
def _logistic_map(z, c, count, max_iter):
    for i in range(max_iter):
        z = np.where(np.abs(z) <= 2, z**2 + c, z)
        
        count += np.abs(z) <= 2
    
    return z, count


def _plot_set(count, xlim, ylim, cmap, axis_labels, **kwargs):
    fig = plt.figure()
    
    plt.imshow(count, extent=[*xlim, *ylim], cmap=cmap, **kwargs)
    plt.axis(axis_labels)
    
    return fig