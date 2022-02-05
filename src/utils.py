from pathlib import Path

import imageio
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap

PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGES_DIR = PROJECT_DIR.joinpath("images")

CMAPS = {
    "uwob": ["#265FD9", "white", "#D9A026", "black"],
    "ultra": [
        (0.0, "#05095c"),
        (0.1, "#0932A4"),
        (0.2, "#50A4E4"),
        (0.4, "white"),
        (0.5, "#FACF31"),
        (0.6, "#B85611"),
        (0.7, "#6C3834"),
        (0.99, "#00065C"),
        (1.0, "black"),
    ],
    "ultra2": [
        (0.0, "#00065C"),
        (0.05, "#0932A4"),
        (0.1, "#50A4E4"),
        (0.2, "white"),
        (0.25, "#FACF31"),
        (0.3, "#B85611"),
        (0.35, "#6C3834"),
        (0.5, "#00065C"),
        (0.55, "#0932A4"),
        (0.6, "#50A4E4"),
        (0.7, "white"),
        (0.75, "#FACF31"),
        (0.8, "#B85611"),
        (0.85, "#6C3834"),
        (0.99, "#00065C"),
        (1.0, "black"),
    ],
    "okabe": [
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
        "#000000",
    ],
}


def linear_cmap(name, N=256):
    assert name in CMAPS.keys(), f"`name` must be one of {set(CMAPS.keys())}"

    cmap = LinearSegmentedColormap.from_list(name, CMAPS[name], N=N, gamma=0.8)

    return cmap


def set_plot_style(axis_lines: bool = False, font: str = None):
    plt.style.use("ggplot")

    plt.rcParams["axes.grid"] = False
    plt.rcParams["axes.edgecolor"] = "#555555"

    if font:
        is_installed = [
            f for f in font_manager.fontManager.ttflist if font in f.name
        ]

        if not is_installed:
            font_files = font_manager.findSystemFonts(fontpaths="font/")

            for font_file in font_files:
                font_manager.fontManager.addfont(font_file)

        plt.rcParams["font.family"] = font


def make_gif(
    input_dir: Path,
    output_file: Path,
    fps: int = 30,
    pause: int = 0,
    back_loop: bool = False,
) -> None:
    """
    Make an animated GIF from PNG images in a directory.

    Parameters
    ----------
    intput_dir : Path
        Directory path containing PNG images.
    output_file : Path
        Gif output file path.
    fps : int, default 30
        Frames per second.
    pause : int, default 0
        Number of repetitions of first and last frame.
    back_loop : bool, default False
        If true, also play GIF backwards after finishing.
    Raises
    ------
    FileNotFoundError
        If no PNG images are found in `intput_dir`.

    Returns
    -------
    None

    """
    if not output_file.suffix:
        output_file = output_file.with_suffix(".gif")

    if output_file.suffix != ".gif":
        raise ValueError("`output_file` extension must be .gif")

    image_files = [file for file in sorted(input_dir.glob("*.png"))]

    if not image_files:
        raise FileNotFoundError("Images not found")

    if pause:
        image_files = (
            image_files[:1] * pause + image_files + image_files[-1:] * pause
        )

    if back_loop:
        image_files = image_files + list(reversed(image_files[1:-1]))

    images = [imageio.imread(file_name) for file_name in image_files]
    imageio.mimwrite(output_file, images, fps=fps)
