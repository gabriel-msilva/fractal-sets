from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.set_plotting import plot_julia
from src.utils import PROJECT_DIR, linear_cmap, make_gif, set_plot_style

images_dir = PROJECT_DIR.joinpath("images")
julia_cmap = linear_cmap("ultra", N=4096)

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
        "cmap": julia_cmap,
        "axis_labels": True,
    }

    fig = plot_julia(**julia_args)

    # DPI ratio for `number of pixels = number_points`
    dpi = julia_args["number_points"] / 3.625
    fig.savefig(image_path, dpi=dpi, pad_inches=0)

    plt.close(fig)


def main(multiprocess: bool = False):
    png_dir = images_dir.joinpath("julia_zoom")

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
        output_file=images_dir.joinpath("julia_zoom.gif"),
        pause=25,
    )


if __name__ == "__main__":
    main(multiprocess=True)
