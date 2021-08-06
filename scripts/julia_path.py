from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt

from src.set_plotting import plot_julia, plot_mandelbrot
from src.utils import PROJECT_DIR, linear_cmap, set_plot_style, make_gif


images_dir = PROJECT_DIR.joinpath('images')
linepaths = {'circumference': False, 'segment': True}
cmap = linear_cmap('ultra', N=4096)

set_plot_style(font='Merriweather')


def get_linepath(name, n_images):
    assert name in {'circumference', 'segment'}
    
    if name == 'circumference':
        n = np.arange(0, 2, 2/n_images)
        c_array = 0.7885 * np.exp(1j * n * np.pi)
    elif name == 'segment':
        c_array = np.linspace(-1j, 1j, n_images)
    return c_array


def plot_linepath(ax, name, color):
    z = get_linepath(name, 100)
    ax.plot(z.real, z.imag, color=color, linestyle='dashed', zorder=1)


def save_plot(c, name, png_path):
    fig, ax = plt.subplots(1, 2)
    
    set_args = {
        'number_points': 600,
        'cmap': cmap,
        'smoothing': True,
        }
    
    plot_mandelbrot(ax=ax[0], **set_args)
    
    plot_linepath(ax[0], name, color='#EB7667')
    ax[0].scatter(x=c.real, y=c.imag, color='#C12D1A', zorder=2)
    
    plot_julia(c, ax=ax[1], vmin=0, vmax=200, **set_args)
    
    ax[0].set(xlabel='Re(c)', ylabel='Im(c)')
    ax[1].set(xlabel='Re(z)', ylabel='Im(z)')
    
    fig.tight_layout()
    
    dpi=set_args['number_points'] / 3.625
    fig.savefig(png_path, dpi=dpi, bbox_inches='tight')
    
    plt.close(fig)


def main(name: str, n_images: int=600, multiprocess: bool=False):
    png_dir = images_dir.joinpath(f'julia_{name}')
    
    if not png_dir.exists():
        png_dir.mkdir(parents=True)
    
    c_array = get_linepath(name, n_images)
    
    d = int(np.log10(n_images)) + 1
    png_paths = [png_dir.joinpath(f'{i:0{d}}.png') for i in range(n_images)]
    
    if multiprocess:
        pool = Pool()
        pool.starmap(save_plot, zip(c_array, [name] * n_images, png_paths))
    else:
        for c, png_path in zip(c_array, png_paths):
            save_plot(c, name, png_path)
    
    make_gif(input_dir=png_dir, 
             output_file=images_dir.joinpath(f'julia_{name}.gif'),
             back_loop=linepaths[name])


if __name__ == '__main__':
    main('circumference', multiprocess=True)
    main('segment', multiprocess=True)
