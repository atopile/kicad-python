# Building kicad-python

First, run `git submodule update --init` to add KiCad's source code as a submodule.

Next install protobuf-compiler

then, install `poetry` and use it to install the required Python dependencies

```sh
$ pip3 install poetry pre-commit
$ poetry shell
$ poetry install
```

Then, to build the library

```sh
$ poetry build
```

# Running examples

Get into a virtual environment for development using Poetry, and then install
the dependencies and the built package:

```sh
$ poetry shell
$ poetry install
```

Then, start KiCad and run:

```sh
$ python3 examples/hello.py
```

This will work if you have a KiCad instance running, with the API server enabled,
and the server is listening at the default location (which will be the case if there
are no other instances of KiCad open at the time).

# Testing changes

Before committing, run `nox`, which will run checks such as linting.

We'll eventually add tests which will run here too :)
