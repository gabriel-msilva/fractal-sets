from pathlib import Path

import typer

PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGES_DIR = PROJECT_DIR.joinpath("images")
STATIC_IMG_DIR = IMAGES_DIR.joinpath("static")
ANIMATED_IMG_DIR = IMAGES_DIR.joinpath("animated")

ARGS = {"multiprocess": typer.Option(True, help="Spawn parallel processes")}
