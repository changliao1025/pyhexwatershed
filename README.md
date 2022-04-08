## `HexWatershed: a mesh independent flow direction model for hydrologic models`

[![DOI](https://zenodo.org/badge/235201194.svg)](https://zenodo.org/badge/latestdoi/235201194)

This Python package provides a <a href="http://www.python.org">`Python`</a> based interface to the underlying `HexWatershed` model.

`HexWatershed` has been compiled and tested on various `64-bit` `Linux` and `Mac` based platforms. 

### `Quickstart`

    Ensure you have a c++ compiler and the cmake utility installed.
    Clone/download + unpack this repository.
    python3 setup.py build_external
    python3 setup.py install
   
    
Note: installation of `HexWatershed` requires a `c++` compiler and the `cmake` utility. Besides, the `GDAL` is required to build the model.
    

### `Acknowledgement`

This work was supported by the Earth System Model Development program areas of the U.S. Department of Energy, Office of Science, Office of Biological and Environmental Research as part of the multi-program, collaborative Integrated Coastal Modeling (ICoM) project. 

### `License`

Please see the LICENSE file.


### `References`

There are a number of publications that describe the algorithms used in `HexWatershed` in detail. If you make use of `HexWatershed` in your work, please consider including a reference to the following:


* Liao, Chang, Tian Zhou, Donghui Xu, Richard Barnes, Gautam Bisht, Hong-Yi Li, Zeli Tan, et al. (02/2022AD) 2022. “Advances In Hexagon Mesh-Based Flow Direction Modeling”. Advances In Water Resources 160. Elsevier BV: 104099. 
https://doi.org/10.1016/j.advwatres.2021.104099.

* Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 128, 104702. https://doi.org/10.1016/j.envsoft.2020.104702

* Liao. C. (2022) Pyflowline: a mesh independent river networks generator for hydrologic models. Zenodo.
https://doi.org/10.5281/zenodo.6407299

* Liao. C. (2022). HexWatershed: a mesh independent flow direction model for hydrologic models (0.1.1). Zenodo. https://doi.org/10.5281/zenodo.6425881


