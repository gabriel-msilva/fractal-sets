from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from cli._utils import ANIMATED_IMG_DIR, ARGS
from src import plot_mandelbrot
from src.utils import animate, linear_cmap, set_plot_style

set_plot_style(font="Merriweather")

mandelbrot_cmap = linear_cmap("ultra", N=4096)
zooming_rate = 1.025


def save_plot(i: int, image_path: Path):
    mandelbrot_args = {
        "number_points": 400,
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


def main(multiprocess: bool = ARGS["multiprocess"]):
    name = "mandelbrot-zoom"
    png_dir = ANIMATED_IMG_DIR.joinpath(name)

    if not png_dir.exists():
        png_dir.mkdir(parents=True)

    n = np.arange(-10, 280)
    png_paths = [png_dir.joinpath(f"{i+10:03}.png") for i in n]

    if multiprocess:
        pool = Pool()
        pool.starmap(save_plot, zip(n, png_paths))
    else:
        for i, png_path in zip(n, png_paths):
            save_plot(i, png_path)

    output_file = png_dir.with_suffix(".gif")

    animate(
        input_dir=png_dir,
        output_file=output_file,
        fps=60,
        pause=20,
        subrectangles=True,
    )
