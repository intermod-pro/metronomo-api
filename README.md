# Metronomo

[![Static Badge](https://img.shields.io/badge/documentation-gray?logo=sphinx)](https://intermod.pro/manuals/metronomo/)
[![PyPI - Version](https://img.shields.io/pypi/v/intermod-metronomo)](https://pypi.org/project/intermod-metronomo/)
[![PyPI - License](https://img.shields.io/pypi/l/intermod-metronomo)](https://github.com/intermod-pro/metronomo-api/blob/master/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://docs.astral.sh/ruff/)

Python API to interact with the Metronomo hardware.

## Quickstart

Install from PyPI using `pip`:
```
python -m pip install intermod-metronomo
```

Control your Metronomo unit from Python using `metronomo.Metronomo`:
```python
from metronomo import Metronomo

with Metronomo("172.23.40.1") as mtr:
    mtr.set_ref_internal()
    mtr.set_out_clk_freq(100e6)
    mtr.sync_out()
```

## Documentation
See the [online documentation](https://intermod.pro/manuals/metronomo/) for setup and installation instruction and for the API reference.
