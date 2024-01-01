# Building kipy

First `git submodule update --init` to add KiCad's source code as a submodule.

Then use the enum_definitions tool in KiCad's tree to generate JSON exports
of all the KiCad enums used by the API:

```sh
$ mkdir kicad-build && cd kicad-build
$ cmake -G Ninja -DKICAD_IPC_API=ON -DKICAD_BUILD_PYTHON_API=ON ../kicad
$ ninja enum_definitions
$ cd ..
$ python3 build-tools/enums.py
```

Note you may need to pass additional args to cmake to get KiCad building;
see the KiCad build documentation for your platform.

To package the Python library for installation:

```sh
$ pip3 install poetry
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
