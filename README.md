# bochscpu-python

[![python 3](https://img.shields.io/badge/python-3.8+-cyan)](https://python.org)
[![Python 3.8+](https://img.shields.io/pypi/v/bochscpu-python.svg)](https://pypi.org/project/bochscpu-python/)
[![Downloads](https://static.pepy.tech/badge/bochscpu-python)](https://pepy.tech/project/bochscpu-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 
[![Licence MIT](https://img.shields.io/packagist/l/doctrine/orm.svg?maxAge=2592000?style=plastic)](https://github.com/hugsy/bochscpu-python/blob/main/LICENSE)


Python bindings for [@yrp](https://github.com/yrp604/)'s [BochsCPU](https://github.com/yrp604/bochscpu) using [FFI](https://github.com/yrp604/bochscpu-ffi)

![image](https://i.imgur.com/YvXg2Tz.png)

## Install

`bochscpu-python` requires a Python environment of 3.8 or more recent only.

### Via PyPI (preferred)

By far the simplest way to get things up and running is using the [stable packaged version](https://pypi.org/project/bochscpu-python/) on [PyPI](https://pypi.org/)

```bash
python -m pip install bochscpu-python
```


### Via the generated builds

Download the latest working artifact from [the repository Github Actions tab](https://github.com/hugsy/bochscpu-python/actions). Extract the ZIP file, install the `.whl` file you'll find inside the `wheel` folder.

```bash
python -m pip install wheel/bochscpu-$version-$os-$arch.whl
```

### From the source repository

Fairly straight forward:

```bash
python -m pip install .
```

Or without cloning

```bash
python -m pip install git+https://github.com/hugsy/bochscpu-python.git#egg=bochscpu-python
```

Note that this approach will require you to have all the building tools necessary installed (as described below)

## Build

### Requirements

 * Python 3.8+ (with development kit)
 * `cmake`
 * `pip`
 * a C++20 compatible compiler (tested `cl` for Windows, `clang` for Linux) 

### Steps

 * Build BochsCPU, BochsCPU-FFI, and BochsCPU-Build following the instructions on their respective pages
 * ... Alternatively BochsCPU-FFI for Windows & Linux libraries object files can be downloaded from the [`build` Github Actions](https://github.com/hugsy/bochscpu-python/actions/workflows/build.yml?query=branch%3Amain+is%3Asuccess+event%3Apush)
 * Move the `*.lib` in `bochscpu/lib/<BuildType>` (where `BuildType` can be `Debug`, `Release`, `RelWithDebInfo`, etc.)
 * Install the requirements: `python -m pip install -r requirements.txt`
 * Build with `cmake`
   This will generate the bochscpu `pyd` file (and its PDB) which you can import from a Python session with `import bochscpu`.
 * ... Alternatively you can also generate a `.whl` from the root of the project:

```bash
python -m pip wheel . 
```

## Usage

Just import the `bochscpu` module and let the fun begin! Installing the package will also install interface files, allowing modern IDEs (VSCode, PyCharm, etc.) to offer useful completion.

## Enjoy 🍻

## TODO

 * [ ] Add more complete examples
 * [ ] Add basic usage examples
 * [ ] Add API docs 


