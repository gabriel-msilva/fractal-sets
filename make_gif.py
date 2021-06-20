from pathlib import Path

import click
import imageio

from src.utils import DIR_TYPE, FILE_TYPE

@click.command()
@click.argument('intput_dir', type=DIR_TYPE)
@click.argument('output_file', type=FILE_TYPE)
@click.argument('fps', type=click.INT, default=30)
def main(intput_dir: Path, output_file: str, fps: int):
    image_files = [file for file in sorted(intput_dir.glob('*.png'))]
    
    if not image_files:
        raise FileNotFoundError('Images not found')
    
    images = [imageio.imread(file_name) for file_name in image_files]
    imageio.mimwrite(output_file, images, fps=fps)
    
    
if __name__ == '__main__':
    main()
