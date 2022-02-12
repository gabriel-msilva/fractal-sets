fractal-sets
============

Plot [Mandelbrot](https://en.wikipedia.org/wiki/Mandelbrot_set) and quadratic [Julia](https://en.wikipedia.org/wiki/Julia_set) sets. This code was used for my [blog post](https://gabriel-msilva.github.io/post/2022-02-08-mandelbrot-and-julia-sets/).

Performance optimized with [numba](https://numba.pydata.org/) and parallelized with [multiprocessing](https://docs.python.org/3/library/multiprocessing.html).

```
├── cli  : Command line interface for plot scripts (blog post)
├── font : Merriweather font used in plots
└── src  : Functions to plot Mandelbrot and Julia sets
```

## Installation

Running environment:

```
conda create
conda activate
```

```
pip install -r requirements.txt
```

Development environment:

```
make conda-env
make pre-commit
```
