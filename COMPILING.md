# Building kicad-python

First, install `poetry` and use it to install the required Python dependencies

```sh
$ pip3 install poetry
$ poetry shell
$ poetry install
```

Next, run `git submodule update --init` to add KiCad's source code as a submodule.

Then use the enum_definitions tool in KiCad's tree to generate JSON exports
of all the KiCad enums used by the API:

```sh
$ mkdir kicad-build && cd kicad-build
$ cmake -G Ninja -DKICAD_IPC_API=ON -DKICAD_BUILD_ENUM_EXPORTER=ON ../kicad
$ ninja enum_definitions
$ cd ..
$ python tools/enums.py
$ python tools/generate_protos.py
```

Note you may need to pass additional args to CMake to get KiCad building;
see the KiCad build documentation for your platform at dev-docs.kicad.org.

After you have initially cloned this repository, to update in the future, run

```sh
$ git pull
$ git submodule update
$ python tools/enums.py
$ python tools/generate_protos.py
```

(at least, until we get this working inside a `build.py`)

To package the Python library for installation:

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

Then you can do something like

```sh
$ python3 examples/layer_indicator/layer_indicator.py
```

This will work if you have a KiCad instance running, with the API server enabled,
and the server is listening at the default location (which will be the case if there
are no other instances of KiCad open at the time).

# Testing changes

Before committing, run `nox`, which will run checks such as linting.

We'll eventually add tests which will run here too :)
