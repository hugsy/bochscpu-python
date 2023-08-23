# bochscpu-python

![python 3](https://img.shields.io/badge/python-3.8+-cyan)
![Python 3.8+](https://img.shields.io/pypi/v/bochscpu-python.svg)
[![Downloads](https://static.pepy.tech/badge/bochscpu-python)](https://pepy.tech/project/bochscpu-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 
[![Licence MIT](https://img.shields.io/packagist/l/doctrine/orm.svg?maxAge=2592000?style=plastic)](https://github.com/hugsy/bochscpu-python/blob/main/LICENSE)


Python bindings for [@yrp](https://github.com/yrp604/)'s [BochsCPU](https://github.com/yrp604/bochscpu) using [FFI](https://github.com/yrp604/bochscpu-ffi)

![image](https://i.imgur.com/YvXg2Tz.png)

## Build

 * Build BochsCPU, BochsCPU-FFI, and BochsCPU-Build following the instructions on their pages
   * Alternatively BochsCPU-FFI lib object files can be downloaded from the [`build` Github Actions](https://github.com/hugsy/bochscpu-python/actions/workflows/build.yml?query=branch%3Amain+is%3Asuccess+event%3Apush)
 * Move the `*.lib` in `bochscpu/lib/<BuildType>` (where `BuildType` can be `Debug`, `Release`, `RelWithDebInfo`, etc.)
 * Install the requirements: `python -m pip install -r requirements.txt`
 * Build with `cmake`
   This will generate the bochscpu `pyd` file (and its PDB) which you can import from a Python session with `import bochscpu`.
 * You can also generate a `.whl`:

```
python -m pip wheel . 
```

## Install

### From the source repository

```
python -m pip install .
```

Or without cloning

```
python -m pip install git+https://github.com/hugsy/bochscpu-python.git#egg=bochscpu-python
```


### Via PyPI

```
python -m pip install bochscpu-python
```


### Via the generated builds

Download the latest working artifact from [the repository Github Actions tab]. Extract the ZIP file, install the `.whl` file you'll find inside the `wheel` folder.

```
python -m pip install wheel/bochscpu-$version-$os-$arch.whl
```


## Usage

Just import the `bochscpu` module and let the fun begin!

Enjoy 🍻
