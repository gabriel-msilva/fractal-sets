import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from src.set_plotting import plot_julia, plot_mandelbrot
from src.utils import PROJECT_DIR, linear_cmap, set_plot_style

images_dir = PROJECT_DIR.joinpath("images")
set_plot_style(font="Merriweather")


# Julia set -------------------------------------------------------------------
fig, ax = plt.subplots(1, 2, sharey=True)

julia_args = {
    "max_iter": 100,
    "number_points": 600,
    "cmap": linear_cmap("ultra", N=4096),
    "smoothing": True,
}

plot_julia(c=-1, ax=ax[0], **julia_args)
ax[0].set(title="c = -1", xlabel="Re(z)", ylabel="Im(z)")

plot_julia(c=1j, ax=ax[1], **julia_args)
ax[1].set(title="c = i", xlabel="Re(z)")

plt.savefig(
    images_dir.joinpath("julia_set.png"),
    dpi=julia_args["number_points"] / 3.625,
    bbox_inches="tight",
)


# Mandelbrot set --------------------------------------------------------------
plot_mandelbrot(number_points=600, axis_labels=True, cmap="gray_r")
plt.xlabel("Re(c)")
plt.ylabel("Im(c)")

file_path = images_dir.joinpath("mandelbrot_bw.png")
plt.savefig(file_path, dpi=200, bbox_inches="tight")


# Colored Mandelbrot set ------------------------------------------------------
mandelbrot_args = {
    "max_iter": 100,
    "number_points": 600,
    "axis_labels": True,
    "smoothing": True,
    "cmap": linear_cmap("ultra", N=4096),
}

fig = plot_mandelbrot(**mandelbrot_args)

plt.colorbar()
plt.xlabel("Re(c)")
plt.ylabel("Im(c)")

plt.savefig(
    images_dir.joinpath("mandelbrot_set.png"),
    dpi=mandelbrot_args["number_points"] / 3,
    bbox_inches="tight",
)


# Mandelbrot zoom -------------------------------------------------------------
def draw_box(ax, center, zoom, color=None, **kwargs):
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


fig, ax = plt.subplots(1, 3)

plot_mandelbrot(ax=ax[0], **mandelbrot_args)
plot_mandelbrot(center=-0.12 + 0.85j, zoom=6, ax=ax[1], **mandelbrot_args)
plot_mandelbrot(center=-0.16 + 1.035j, zoom=100, ax=ax[2], **mandelbrot_args)

ax[0].axis("off")
ax[1].axis("off")
ax[2].axis("off")

draw_box(ax[0], center=-0.12 + 0.85j, zoom=6, color="#C12D1A")
draw_box(ax[1], center=-0.16 + 1.035j, zoom=100, color="#C12D1A")

plt.savefig(
    images_dir.joinpath("mandelbrot_zoom.png"),
    dpi=439,
    bbox_inches="tight",
    pad_inches=0,
)


# Mandelbrot smoothing --------------------------------------------------------
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

plt.savefig(
    images_dir.joinpath("mandelbrot_smoothing.png"),
    dpi=mandelbrot_args["number_points"] / 3.625,
    bbox_inches="tight",
)
