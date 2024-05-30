"""
Module: configurator.py

Handles configuration using [Tom's Obvious Minimal Language](https://toml.io/en/) files.
"""

import tomllib as _tomllib
from pathlib import Path as _Path
from typing import Any as _Any

from loguru import logger as _logger

# Public objects
__all__: list[str] = [
    # VSCode: Sort lines in descending order
    "load_config",
]


def _load_toml(
    file_path: str,
) -> dict[str, _Any]:
    """
    Load and parse a TOML file using explicit file paths.

    Args:
        file_path (str): Path to the TOML file to load (e.g., "~/configs/default.toml").

    Raises:
        IOError: If failed to parse or load the TOML file.

    Returns:
        dict[str, Any]: Dictionary containing the data from the TOML file.
    """
    _logger.debug(
        f"Loading TOML file from '{file_path}'",
    )
    try:
        with open(file_path, mode="rb") as file:
            return _tomllib.load(file)
    except _tomllib.TOMLDecodeError as e:
        raise OSError(
            f"Failed to parse TOML file at '{file_path}': {e}",
        ) from e
    except Exception as e:
        raise OSError(
            f"Failed to load TOML file at '{file_path}': {e}",
        ) from e


def load_config(
    default_file_path: str,
    custom_file_path: str,
) -> dict[str, _Any]:
    """
    Load a custom configuration from a TOML file using explicit file paths.

    First, the `default_file_path` is loaded, then it is overwritten by the `custom_file_path`.

    Args:
        default_file_path (str): Path to the default TOML config file to load, must include a file extension (e.g., "~/configs/default.toml").
        custom_file_path (str): Path to the custom TOML config file to load that will overwrite the default config file, must include a file extension (e.g., "~/configs/bert.toml").

    Raises:
        FileNotFoundError: If the configuration directory does not exist.
        ValueError: If a key in the custom configuration is not found in the default configuration.

    Returns:
        dict[str, Any]: Dictionary containing the merged configuration.

    Notes:
        - All config files are expected to be in the "root/configs" directory.
        - The structure of the "configs" directory should be similar to the following example:

            ```
            .
            └── configs
                ├── default.toml
                └── bert.toml
            ```
    """
    # Check if default config exists
    if not _Path(default_file_path).exists():
        raise FileNotFoundError(
            f"Default configuration file '{default_file_path}' does not exist, please create it",
        )

    # Load default config
    default_config: dict[str, _Any] = _load_toml(default_file_path)
    _logger.debug(
        f"Loaded default config: {default_config}",
    )

    # Check if custom config exists
    if not _Path(custom_file_path).exists():
        raise FileNotFoundError(
            f"Custom configuration file '{custom_file_path}' does not exist, please create it",
        )

    # Load custom config
    custom_config: dict[str, _Any] = _load_toml(custom_file_path)
    _logger.debug(
        f"Loaded custom config: {custom_config}",
    )

    # Overwrite default config with custom config
    _logger.debug(
        "Overwriting default config with custom config...",
    )
    for key, value in custom_config.items():
        # Check if key in default_config
        if key not in default_config:
            raise ValueError(
                f"Custom key '{key}' not found in default config, cannot overwrite it, please remove it",
            )

        # Log the value being overwritten
        _logger.info(
            f"Overwriting '{key}': '{default_config[key]}' -> '{value}'",
        )

        # Overwrite the value
        default_config[key] = value

    # Log results
    _logger.debug(
        f"Merged config: {default_config}",
    )

    return default_config


# If this file is run directly, run the tests
if __name__ == "__main__":
    import sys as _sys
    import unittest as _unittest
    from tempfile import NamedTemporaryFile as _NamedTemporaryFile

    # Set the log level to INFO (comment out these lines to see DEBUG level messages)
    _logger.remove()
    _logger.add(_sys.stdout, level="INFO")

    class TestLoadConfig(_unittest.TestCase):
        def test_load_config(
            self,
        ) -> None:
            """
            Ensure that the config loader can load the default config and overwrite it with a custom config.
            """
            # Log the name of the test
            _logger.info(
                "Running test: test_load_config",
            )

            # Create a temporary file for the default configuration
            with _NamedTemporaryFile(mode="w", encoding="utf-8") as default_config_file:
                # Write the default configuration to the file
                default_str: str = 'brand = "Nissan"\nmodel = "180SX"'
                default_config_file.write(default_str)
                default_config_file.seek(0)

                # Create a temporary file for the custom configuration
                with _NamedTemporaryFile(
                    mode="w", encoding="utf-8"
                ) as custom_config_file:
                    # Write the custom configuration to the file
                    custom_str: str = 'model = "Silvia S15"'
                    custom_config_file.write(custom_str)
                    custom_config_file.seek(0)

                    # Load the default configuration, overwrite it with the custom configuration
                    merged_config: dict[str, _Any] = load_config(
                        default_file_path=default_config_file.name,
                        custom_file_path=custom_config_file.name,  # Overwrite "model" with "Silvia S15"
                    )

                    # Assert that the final configuration is as expected
                    self.assertEqual(
                        merged_config,
                        {"brand": "Nissan", "model": "Silvia S15"},
                    )

    # Run the tests
    _unittest.main()
