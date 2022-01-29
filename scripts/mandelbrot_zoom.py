from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.set_plotting import plot_mandelbrot
from src.utils import PROJECT_DIR, linear_cmap, make_gif, set_plot_style

images_dir = PROJECT_DIR.joinpath("images")
mandelbrot_cmap = linear_cmap("ultra", N=4096)

set_plot_style(font="Merriweather")


def main(multiprocess: bool = False):
    png_dir = images_dir.joinpath("mandelbrot_zoom")

    if not png_dir.exists():
        png_dir.mkdir(parents=True)

    n = np.arange(-10, 280)

    png_paths = [png_dir.joinpath(f"{i+10:03}.png") for i in n]

    if multiprocess:
        pool = Pool()
        pool.starmap(save_mandelbrot, zip(n, png_paths))
    else:
        for i, png_path in zip(n, png_paths):
            save_mandelbrot(i, png_path)

    make_gif(
        input_dir=png_dir,
        output_file=images_dir.joinpath("mandelbrot_zoom.gif"),
        fps=60,
        pause=20,
    )


def save_mandelbrot(i: int, image_path: Path):
    zooming_rate = 1.025

    mandelbrot_args = {
        "number_points": 600,
        "center": -1.4177,
        "zoom": zooming_rate**i,
        "max_iter": 200 + 10 * i,
        "axis_labels": True,
        "smoothing": True,
        "cmap": mandelbrot_cmap,
    }

    fig = plot_mandelbrot(**mandelbrot_args)

    dpi = mandelbrot_args["number_points"] / 3.695
    fig.savefig(image_path, dpi=dpi, pad_inches=0)

    plt.close(fig)


if __name__ == "__main__":
    main(multiprocess=True)
