---
hide:
  - navigation
---

# Installation

The best way to install pynapple is with pip within a new [conda](https://docs.conda.io/en/latest/) environment :

    
``` {.sourceCode .shell}
$ conda create --name pynapple pip python=3.8
$ conda activate pynapple
$ pip install pynapple
```

or directly from the source code:

``` {.sourceCode .shell}
$ conda create --name pynapple pip python=3.8
$ conda activate pynapple
$ # clone the repository
$ git clone https://github.com/pynapple-org/pynapple.git
$ cd pynapple
$ # Install in editable mode with `-e` or, equivalently, `--editable`
$ pip install -e .
```
> **Note**
> The package is now using a pyproject.toml file for installation and dependencies management. If you want to run the tests, use pip install -e .[dev]

This procedure will install all the dependencies including 

-   pandas
-   numpy
-   scipy
-   numba
-   pynwb 2.0
-   tabulate
-   h5py


