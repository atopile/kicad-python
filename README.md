# KiCad API Python Bindings

`kicad-python` is the official Python bindings for the [KiCad](https://kicad.org) IPC API.  This
library makes it possible to develop scripts and tools that interact with a running KiCad session.

The KiCad IPC API can be considered in "public beta" state with the release of KiCad 9 (currently
planned for on or around February 1, 2025).  The existing SWIG-based Python bindings for KiCad's
PCB editor still exist in KiCad 9, but are in maintenance mode and will not be expanded.

For more information about the IPC API, please see the [KiCad developer documentation](https://dev-docs.kicad.org).

> Note: Version 0.0.2 and prior of this package are an obsolete earlier effort and are unrelated to
> this codebase.

## Requirements

Using the IPC API requires a suitable version of KiCad (9.0 or higher) and requires that KiCad be
running with the API server enabled in Preferences > Plugins.  This package also depends on the
`protobuf` and `pynng` packages for communication with KiCad.

> Note: Unlike the SWIG-based Python bindings, the IPC API requires communication with a running
> instance of KiCad.  It is not possible to use `kicad-python` to manipulate KiCad design files
> without KiCad running.

## Contributing

At the moment, these bindings are being developed in parallel with the IPC API itself, and
development is being coordinated by the KiCad team (main point of contact: Jon Evans / @craftyjon).
Expect rapid change and instability during this development period, and please do not send merge
requests without discussing your idea for changes with the team ahead of time.

Once the initial stable API is released (planned for KiCad 9.0 in February 2025), this Python
library will also have its first stable release and be considered fully supported.  Until that
time, please consider this a development preview.

## Building

See COMPILING.md

## API Documentation

There is no documentation separate from the code comments and examples yet, sorry!  This will be
more of a priority once the KiCad 9 release is stable.

## Examples

Check out the repository for some example scripts that may serve as a starting point.

## Release History

### 0.1.1 (December 24, 2024)

- Bump dependency versions to fix compilation with newer protoc

### 0.1.0 (December 21, 2024)

*Corresponding KiCad version: 9.0.0-rc1*

First formal release of the new IPC-API version of this package.  Contains support for most of the
KiCad API functionality that is currently exposed, which is focused around the PCB editor to enable
a transition path from existing SWIG-based plugins.

Caveats / Known Issues:

- Compatibility limited to Python 3.9 ~ 3.12 due to `pynng` not yet being updated for 3.13
