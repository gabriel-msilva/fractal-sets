from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from cli._utils import ANIMATED_IMG_DIR, ARGS
from src import plot_mandelbrot
from src.utils import linear_cmap, make_gif

mandelbrot_cmap = linear_cmap("ultra", N=4096)


def save_plot(i: int, image_path: Path):
    zooming_rate = 1.04

    mandelbrot_args = {
        "center": (
            -0.743643887037158704752191506114774
            + 0.131825904205311970493132056385139j
        ),
        "zoom": zooming_rate**i,
        "max_iter": np.sqrt(zooming_rate**i) + 200,
        "number_points": 600,
        "smoothing": True,
        "cmap": mandelbrot_cmap,
        "interpolation": "antialiased",
    }

    fig = plot_mandelbrot(**mandelbrot_args)

    # DPI ratio for `number of pixels = number_points`
    dpi = mandelbrot_args["number_points"] / 3.695
    fig.savefig(
        image_path,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )

    plt.close(fig)


def main(multiprocess: bool = ARGS["multiprocess"]):
    name = "mandelbrot_zoom2"
    png_dir = ANIMATED_IMG_DIR.joinpath(name)

    if not png_dir.exists():
        png_dir.mkdir(parents=True)

    n = np.arange(735)
    png_paths = [png_dir.joinpath(f"{i:03}.png") for i in n]

    if multiprocess:
        pool = Pool()
        pool.starmap(save_plot, zip(n, png_paths))
    else:
        for i, png_path in zip(n, png_paths):
            save_plot(i, png_path)

    make_gif(
        input_dir=png_dir,
        output_file=ANIMATED_IMG_DIR.joinpath(name),
        pause=20,
    )
