from pathlib import Path

import click
from matplotlib.colors import LinearSegmentedColormap


DIR_TYPE = click.Path(file_okay=False, resolve_path=True, path_type=Path)
FILE_TYPE = click.Path(exists=False, dir_okay=False, writable=True, 
                       resolve_path=True, path_type=Path)

CMAPS = {
    'uwob': ['darkblue', 'white', 'darkorange', 'black', ], 
    'okabe': ['#E69F00', '#56B4E9', '#009E73', '#F0E442', 
              '#0072B2', '#D55E00', '#CC79A7', '#000000'], 
    }

CMAPS['rev_okabe'] = list(reversed(CMAPS['okabe']))


def linear_cmap(name):
    assert name in CMAPS.keys(), f'`name` must be one of {set(CMAPS.keys())}'
    
    return LinearSegmentedColormap.from_list(name, CMAPS[name])
