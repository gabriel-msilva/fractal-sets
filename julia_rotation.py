from pathlib import Path
from multiprocessing import Pool

import click
import numpy as np
import matplotlib.pyplot as plt

from src.set_plotting import plot_julia
from src.utils import DIR_TYPE, linear_cmap


@click.command()
@click.argument('output_dir', type=DIR_TYPE)
@click.argument('n_images', type=click.INT, default=200)
@click.option('--multiprocess', is_flag=True, default=False, help='Turn on multiprocessing')
def main(output_dir: Path, n_images: int=200, multiprocess: bool=False):
    if not output_dir.exists():
        output_dir.mkdir()
    
    n = np.arange(0, 2, 2/n_images)
    c_array = 0.7885 * np.exp(1j * n * np.pi)
    
    n_zeroes = int(np.log10(n_images)) + 1
    image_paths = [output_dir.joinpath(f'{i:0{n_zeroes}}.png') 
                   for i in range(n_images)]
    
    if multiprocess:
        pool = Pool()
        pool.starmap(save_julia, zip(c_array, image_paths))
    else:
        for c, image_path in c_array, image_paths:
            save_julia(c, image_path)
    

def save_julia(c: int, image_path: Path):
    julia_args = {
        'c': c,
        'max_iter': 100,
        'number_points': 600,
        'cmap': linear_cmap('rev_okabe'),
        'vmin': 0,
        'vmax': 100
        }
    
    fig = plot_julia(**julia_args)
    
    # DPI ratio for number of pixels = number_points
    dpi = julia_args['number_points'] * (100/370)
    fig.savefig(image_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    
    plt.close(fig)


if __name__ == '__main__':
    main()