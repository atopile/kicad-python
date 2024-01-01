# KiCad API Python Bindings

`kipy` is the official Python bindings for the [KiCad](https://kicad.org) API.  This library makes
it possible to develop scripts and tools that interact with a running KiCad session.

## Building

First `git submodule update --init` to add KiCad's source code as a submodule.

```
cd kicad
mkdir kicad-build && cd kicad-build
cmake -G Ninja -DKICAD_IPC_API=ON -DKICAD_BUILD_PYTHON_API=ON ../kicad
ninja python_enums
```

Note you may need to pass additional args to cmake to get KiCad building;
see the KiCad build documentation for your platform.

## API Documentation

There is no documentation yet, sorry.

## Examples

Check out the repository for some example scripts that may serve as a starting point.
