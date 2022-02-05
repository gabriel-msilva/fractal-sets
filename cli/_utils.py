import typer

from src.utils import IMAGES_DIR

STATIC_IMG_DIR = IMAGES_DIR.joinpath("static")
ANIMATED_IMG_DIR = IMAGES_DIR.joinpath("animated")

ARGS = {"multiprocess": typer.Option(True, help="Spawn parallel processes")}
