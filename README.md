# bochscpu-python

Python bindings for [@yrp](https://github.com/yrp604/)'s [BochsCPU](https://github.com/yrp604/bochscpu) using [FFI](https://github.com/yrp604/bochscpu-ffi)

![image](https://github.com/hugsy/bochscpu-python/assets/590234/0cdddc04-d291-470f-8dfe-80b1604d612b)

## Build

 * Build BochsCPU, BochsCPU-FFI, and BochsCPU-Build following the instructions on their pages
 * Move the `*.lib` in `bochscpu/lib/<BuildType>` (where `BuildType` can be `Debug`, `Release`, `RelWithDebInfo`, etc.)
 * Install the requirements: `python -m pip install -r requirements.txt`
 * Build with `cmake`
   This will generate the bochscpu `pyd` file (and its PDB) which you can import from a Python session with `import bochscpu`.
 * You can also generate a `.whl`:

```
mkdir wheel
python -m pip wheel . -w .\wheel\
```

## Install

```
python -m pip install .
```

## TODO

 - Automated build via CI
 - PyPI package via CI
