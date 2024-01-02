# Building kipy

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
$ poetry run python tools/enums.py
$ poetry run python tools/generate_protos.py
```

Note you may need to pass additional args to CMake to get KiCad building;
see the KiCad build documentation for your platform at dev-docs.kicad.org.

To package the Python library for installation:

```sh
$ poetry build
```

# Testing

The easiest way is to install the built module into whatever Python you are running:

```sh
$ pip3 install dist/kipy-<whatever>.whl
```

Then you can do something like

```sh
$ pip3 install pyqt6
$ python3 examples/tracks.py
```
