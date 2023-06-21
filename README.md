fractal-sets
============

<img src="https://github.com/gabriel-msilva/melloc/blob/b58df38fd4ec1c4c6c2f51b160ea1cc6a500f1af/content/post/2022-02-08-mandelbrot-and-julia-sets/figures/static/mandelbrot-colored.png" alt="Mandelbrot set" width="50%" />

Plot [Mandelbrot](https://en.wikipedia.org/wiki/Mandelbrot_set) and quadratic [Julia](https://en.wikipedia.org/wiki/Julia_set) sets. This code was used for my [blog post](https://gabriel-msilva.github.io/melloc/post/2022-02-08-mandelbrot-and-julia-sets/).

Performance optimized with [numba](https://numba.pydata.org/) and parallelized with [multiprocessing](https://docs.python.org/3/library/multiprocessing.html).

```
├── cli  : Command line interface for plot scripts (blog post)
├── font : Merriweather font used in plots
└── src  : Functions to plot Mandelbrot and Julia sets
```

## Installation

Running environment:

```
conda env create
conda activate
```

or
 
```
pip install -r requirements.txt
```

Development environment:

```
make conda-env
make pre-commit
```
