"""
Module: utils.py

Handles repeating code that is used in different parts of the project.
"""

from pathlib import Path as _Path
from time import time as _time

from loguru import logger as _logger

# Public objects
__all__: list[str] = [
    # VSCode: Sort lines in descending order
    "create_timestamped_log_file",
]


def create_timestamped_log_file(
    script_name: str,
    output_directory: _Path,
) -> None:
    """
    Initialize a logger that logs to a timestamped log file in the output directory.

    E.g., "~/logs/train_1717095105.731416.log".

    Args:
        script_name (str): Name of the script (e.g., "train.py").
        output_directory (Path): Path to the output directory (e.g., "~/logs").
    """
    # Strip the file extension from the script name (e.g., "~/scripts/train.py" -> "train"), add the current time in seconds since the Epoch to the log file name, add ".log" at the end
    file_name: str = f"{_Path(script_name).stem}_{_time()}.log"
    _logger.add(str(output_directory / file_name))
