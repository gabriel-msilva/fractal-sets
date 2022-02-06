import typer

from cli._utils import ANIMATED_IMG_DIR
from cli.scripts import (
    julia_path,
    julia_zoom,
    mandelbrot_deep_zoom,
    mandelbrot_zoom,
)

if not ANIMATED_IMG_DIR.exists():
    ANIMATED_IMG_DIR.mkdir()

julia_app = typer.Typer()
julia_app.command("path")(julia_path)
julia_app.command("zoom")(julia_zoom)

mandelbrot_app = typer.Typer()
mandelbrot_app.command("zoom")(mandelbrot_zoom)
mandelbrot_app.command("deep-zoom")(mandelbrot_deep_zoom)

app = typer.Typer()
app.add_typer(julia_app, name="julia")
app.add_typer(mandelbrot_app, name="mandelbrot")


if __name__ == "__main__":
    app()
