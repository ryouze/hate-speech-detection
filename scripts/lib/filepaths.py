"""
Module: filepaths.py

Stores relative filepaths used by the project.
"""

from pathlib import Path as _Path

# Public objects
__all__: list[str] = [
    # VSCode: Sort lines in descending order
    "configs",
    "datasets",
    "logs",
    "models",
    "modules",
    "root",
]

# ------------------------------------------------------------------------------
# Path to the root directory of the project (root/)
# This assumes that this file is located in the `root/scripts/lib/` directory
root: _Path = _Path(__file__).resolve().parents[2]
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Path: root/configs/
configs: _Path = root / "configs"

# Path: root/datasets/
datasets: _Path = root / "datasets"

# Path: root/logs/
logs: _Path = root / "logs"

# Path: root/models/
models: _Path = root / "models"

# Path: root/modules/
modules: _Path = root / "modules"

# ------------------------------------------------------------------------------
# Recursively create the directories if they don't exist
for directory in (configs, datasets, logs, models, modules):
    directory.mkdir(parents=True, exist_ok=True)
