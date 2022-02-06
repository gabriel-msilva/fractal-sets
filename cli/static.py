import matplotlib.pyplot as plt
import typer
from matplotlib.patches import Rectangle

from cli._utils import STATIC_IMG_DIR
from src.plotting import plot_julia, plot_mandelbrot
from src.utils import linear_cmap, set_plot_style

if not STATIC_IMG_DIR.exists():
    STATIC_IMG_DIR.mkdir()

JULIA_ARGS = {
    "max_iter": 100,
    "number_points": 600,
    "cmap": linear_cmap("ultra", N=4096),
    "smoothing": True,
}

MANDELBROT_ARGS = {
    "max_iter": 100,
    "number_points": 600,
    "axis_labels": True,
    "smoothing": True,
    "cmap": linear_cmap("ultra", N=4096),
}


set_plot_style(font="Merriweather")
app = typer.Typer(help="Save static plot images as PNG at images/ directory.")

mandelbrot_app = typer.Typer()
app.add_typer(mandelbrot_app, name="mandelbrot")


def _save_fig(file_name: str, dpi: float, **kwargs):
    plt.savefig(
        STATIC_IMG_DIR.joinpath(file_name),
        dpi=dpi,
        bbox_inches="tight",
    )


@app.command()
def julia():
    fig, ax = plt.subplots(1, 2, sharey=True)

    plot_julia(c=-1, ax=ax[0], **JULIA_ARGS)
    ax[0].set(title="c = -1", xlabel="Re(z)", ylabel="Im(z)")

    plot_julia(c=1j, ax=ax[1], **JULIA_ARGS)
    ax[1].set(title="c = i", xlabel="Re(z)")

    dpi = JULIA_ARGS["number_points"] / 3.625
    _save_fig("julia-set.png", dpi)


@mandelbrot_app.command("bw")
def mandelbrot_bw():
    plot_mandelbrot(
        number_points=MANDELBROT_ARGS["number_points"],
        axis_labels=MANDELBROT_ARGS["axis_labels"],
        cmap="gray_r",
    )

    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")

    _save_fig("mandelbrot-bw.png", dpi=200)


@mandelbrot_app.command("colored")
def mandelbrot_colored():
    fig = plot_mandelbrot(**MANDELBROT_ARGS)

    plt.colorbar()
    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")

    dpi = MANDELBROT_ARGS["number_points"] / 3
    _save_fig("mandelbrot-colored.png", dpi)

    plt.close(fig)


def _draw_box(ax, center, zoom, color=None, **kwargs):
    a = 3 / zoom

    ax.add_patch(
        Rectangle(
            (center.real - a / 2, center.imag - a / 2),
            width=a,
            height=a,
            edgecolor=color,
            fill=False,
            **kwargs
        )
    )


@mandelbrot_app.command("zoom")
def mandelbrot_zoom():
    fig, ax = plt.subplots(1, 3)

    plot_mandelbrot(ax=ax[0], **MANDELBROT_ARGS)
    plot_mandelbrot(center=-0.12 + 0.85j, zoom=6, ax=ax[1], **MANDELBROT_ARGS)
    plot_mandelbrot(
        center=-0.16 + 1.035j, zoom=100, ax=ax[2], **MANDELBROT_ARGS
    )

    ax[0].set_title("(a)")
    ax[0].axis("off")

    ax[1].set_title("(b)")
    ax[1].axis("off")

    ax[2].set_title("(c)")
    ax[2].axis("off")

    _draw_box(ax[0], center=-0.12 + 0.85j, zoom=6, color="#C12D1A")
    _draw_box(ax[1], center=-0.16 + 1.035j, zoom=100, color="#C12D1A")

    _save_fig("mandelbrot-zoom.png", dpi=439, pad_inches=0, transparent=True)


@mandelbrot_app.command("smoothing")
def mandelbrot_smoothing():
    fig, ax = plt.subplots(1, 2)

    zoom_args = {
        "max_iter": 100,
        "center": 0.3,
        "zoom": 20,
        "cmap": linear_cmap("ultra", N=4096),
    }

    plot_mandelbrot(ax=ax[0], **zoom_args)
    plot_mandelbrot(ax=ax[1], smoothing=True, **zoom_args)

    ax[0].set_title("(a)")
    ax[0].axis("off")

    ax[1].set_title("(b)")
    ax[1].axis("off")

    plt.tight_layout()

    dpi = MANDELBROT_ARGS["number_points"] / 3.625
    _save_fig("mandelbrot-smoothing.png", dpi)


if __name__ == "__main__":
    app()
