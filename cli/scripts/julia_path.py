from enum import Enum
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import typer

from cli._utils import ANIMATED_IMG_DIR, ARGS
from src import plot_julia, plot_mandelbrot
from src.utils import linear_cmap, make_gif, set_plot_style

BACK_LOOP = {"circumference": False, "segment": True}
CMAP = linear_cmap("ultra", N=4096)

set_plot_style(font="Merriweather")


def get_line_path(line_path, n_images):
    assert line_path in {"circumference", "segment"}

    if line_path == "circumference":
        n = np.arange(0, 2, 2 / n_images)
        c_array = 0.7885 * np.exp(1j * n * np.pi)
    elif line_path == "segment":
        c_array = np.linspace(-1j, 1j, n_images)
    return c_array


def plot_line_path(ax, line_path, color):
    z = get_line_path(line_path, 100)
    ax.plot(z.real, z.imag, color=color, linestyle="dashed", zorder=1)


def save_plot(c, line_path, png_path):
    fig, ax = plt.subplots(1, 2)

    set_args = {
        "number_points": 600,
        "cmap": CMAP,
        "smoothing": True,
    }

    plot_mandelbrot(ax=ax[0], **set_args)

    plot_line_path(ax[0], line_path, color="#EB7667")
    ax[0].scatter(x=c.real, y=c.imag, color="#C12D1A", zorder=2)

    plot_julia(c, ax=ax[1], vmin=0, vmax=200, **set_args)

    ax[0].set(xlabel="Re(c)", ylabel="Im(c)")
    ax[1].set(xlabel="Re(z)", ylabel="Im(z)")

    fig.tight_layout()

    dpi = set_args["number_points"] / 3.625
    fig.savefig(png_path, dpi=dpi, bbox_inches="tight", transparent=True)

    plt.close(fig)


class LinePath(str, Enum):
    segment = "segment"
    circumference = "circumference"


def main(
    line_path: LinePath = typer.Argument(..., help="Type of line path"),
    multiprocess: bool = ARGS["multiprocess"],
):
    """Make animated GIF of Julia sets for `c` in a line path."""
    name = f"julia-{line_path}"
    png_dir = ANIMATED_IMG_DIR.joinpath(name)

    if not png_dir.exists():
        png_dir.mkdir(parents=True)

    n_images = 600
    c_array = get_line_path(line_path, n_images)

    d = int(np.log10(n_images)) + 1
    png_paths = [png_dir.joinpath(f"{i:0{d}}.png") for i in range(n_images)]

    if multiprocess:
        pool = Pool()
        pool.starmap(
            save_plot, zip(c_array, [line_path] * n_images, png_paths)
        )
    else:
        for c, png_path in zip(c_array, png_paths):
            save_plot(c, line_path, png_path)

    output_file = png_dir.with_suffix(".gif")
    make_gif(
        input_dir=png_dir,
        output_file=output_file,
        back_loop=BACK_LOOP[line_path],
    )
