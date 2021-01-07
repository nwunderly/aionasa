# ENAE380 Final Project - aionasa


### About the project

An async python wrapper for the NASA open APIs.

Our final project is the aionasa.epic module
This README will be a guide to using that module.


### Requirements

- Python 3.8
- A NASA API key from [api.nasa.gov](https://api.nasa.gov/)
  - without this, the API key `DEMO_KEY` will be used, which has a much more restrictive rate limit.
- Python packages from PyPI:
  - aionasa
  - PySimpleGUI

### Installing

The project branch of aionasa can be installed from source with the command:
```shell
pip install -U git+https://github.com/nwunderly/aionasa@enae380
```
Where `pip` is the pip command relevant to your machine's Python 3.8 installation.
This could be `pip`, `pip3`, `python -m pip`, or `python3 -m pip`.


### Using the CLI/GUI

The GUI tool is launched by running the `aionasa.epic` module as a script, with the `python -m` command.

The `--help` option will give a breakdown of how to use this command:

```shell
python -m aionasa.epic --help
```
