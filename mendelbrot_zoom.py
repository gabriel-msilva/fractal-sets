from pathlib import Path
from multiprocessing import Pool
import timeit

import click
import numpy as np
import matplotlib.pyplot as plt

from src.set_plotting import plot_mendelbrot
from src.utils import DIR_TYPE, linear_cmap


@click.command()
@click.argument('output_dir', type=DIR_TYPE)
@click.argument('start', type=click.INT, default=0)
@click.argument('end', type=click.INT, default=None, required=False)
@click.option('--multiprocess', is_flag=True, default=False, help='Turn on multiprocessing')
def main(output_dir: Path, start: int=0, end: int=None, multiprocess: bool=False):
    if end is None:
        end = start + 1
    
    n = np.arange(start, end)
    
    if not output_dir.exists():
        output_dir.mkdir()
    
    image_paths = [output_dir.joinpath(f'{i:03}.png') for i in n]
    
    tic = timeit.default_timer()
    
    if multiprocess:
        pool = Pool()
        pool.starmap(save_mendelbrot, zip(n, image_paths))
    else:
        for i, image_path in zip(n, image_paths):
            save_mendelbrot(i, image_path)
    
    toc = timeit.default_timer()
    print('Time: ', toc - tic) 
    

def save_mendelbrot(i: int, image_path: Path):
    mendelbrot_args = {
        'center':  (-0.743643887037158704752191506114774 + 
                    0.131825904205311970493132056385139j),
        'zoom': 1.5**i,
        'max_iter': max(np.sqrt(1.5**i), 200),
        'number_points': 300,
        'cmap': linear_cmap('uwob'),
        }
    
    fig = plot_mendelbrot(**mendelbrot_args)
    
    # DPI ratio for number of pixels = number_points
    dpi = mendelbrot_args['number_points'] * (100/301)
    fig.savefig(image_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    
    plt.close(fig)


if __name__ == '__main__':
    main()