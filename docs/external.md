Pynapple has been designed as a lightweight package for representing time series and epochs in system neuroscience.
As such, it can function as a foundational element for other analysis packages handling time series data. Here we keep track of external projects that uses pynapple.


## NEMOS

![image](https://raw.githubusercontent.com/flatironinstitute/nemos/main/docs/assets/glm_features_scheme.svg)

[NeMOs](https://nemos.readthedocs.io/en/stable/) is a statistical modeling framework optimized for systems neuroscience and powered by JAX. It streamlines the process of defining and selecting models, through a collection of easy-to-use methods for feature design.

The core of nemos includes GPU-accelerated, well-tested implementations of standard statistical models, currently focusing on the Generalized Linear Model (GLM). 

Check out this [page](https://nemos.readthedocs.io/en/stable/generated/neural_modeling/) for many examples of neural modelling using nemos and pynapple.

!!! note
	Nemos is build on top of [jax](https://jax.readthedocs.io/en/latest/index.html), a library for high-performance numerical computing.
	To ensure full compatibility with nemos, consider installing [pynajax](https://github.com/pynapple-org/pynajax), a pynapple backend for jax.