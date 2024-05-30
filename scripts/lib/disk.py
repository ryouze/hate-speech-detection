"""
Module: disk.py

Handles disk operations.
"""

from pathlib import Path as _Path
from time import time as _time
from zipfile import ZipFile as _ZipFile

from loguru import logger as _logger

# Public objects
__all__: list[str] = [
    # VSCode: Sort lines in descending order
    "unpack_and_rename",
]


def unpack_and_rename(
    zip_file: _Path,
    password: str,
    file_to_extract: str,
    output_directory: _Path,
    output_file_name: str,
) -> None:
    """
    Unpack the specific file from the `.zip` file with the given password to the output directory and rename it.

    Since each BAN-PL `.zip` file contains only one file, we can extract it and rename it in one step.

    Args:
        zip_file (Path): Path to the `.zip` file (e.g., "~/dataset/BAN-PL_1.zip").
        password (str): Password to the `.zip` file (e.g., "1234").
        file_to_extract (str): The specific file to extract from the zip file.
        output_directory (Path): Path to the output directory (e.g., "~/output").
        output_file_name (str): The new name for the extracted file.

    Raises:
        OSError: If the "zip_file" does not exist or failed to unpack the `.zip` file.
    """
    start: float = _time()
    # Raise if doesn't exist
    if not zip_file.exists():
        raise OSError(
            f"File '{zip_file}' does not exist, try running 'git submodule update --init --recursive'"
        )

    # Unpack the specific file from the `.zip` file into the output directory
    try:
        with _ZipFile(zip_file, "r") as f:
            f.extract(file_to_extract, output_directory, pwd=password.encode())
            # Rename the file
            (output_directory / file_to_extract).rename(
                output_directory / output_file_name
            )
    except Exception as e:
        raise OSError(f"Failed to unpack '{zip_file}' to '{output_directory}': {e}")

    _logger.debug(
        f"Unpacked '{zip_file}' to '{output_directory}' and renamed it to '{output_file_name}', took {round(_time() - start, 2)}s"
    )
