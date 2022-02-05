from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from cli._utils import ANIMATED_IMG_DIR, ARGS
from src import plot_julia
from src.utils import linear_cmap, make_gif, set_plot_style

CMAP = linear_cmap("ultra", N=4096)

set_plot_style(font="Merriweather")


def save_plot(i: int, image_path: Path):
    zooming_rate = 1.05

    julia_args = {
        "c": -1,
        "center": 1.61803398874989,
        "zoom": zooming_rate**i,
        "max_iter": 100,
        "number_points": 600,
        "smoothing": True,
        "cmap": CMAP,
        "axis_labels": True,
    }

    fig = plot_julia(**julia_args)

    # DPI ratio for `number of pixels = number_points`
    dpi = julia_args["number_points"] / 3.625
    fig.savefig(image_path, dpi=dpi, pad_inches=0, transparent=True)

    plt.close(fig)


def main(multiprocess: bool = ARGS["multiprocess"]):
    name = "julia-zoom"
    png_dir = ANIMATED_IMG_DIR.joinpath(name)

    if not png_dir.exists():
        png_dir.mkdir(parents=True)

    n = np.arange(600)

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
        pause=25,
    )
