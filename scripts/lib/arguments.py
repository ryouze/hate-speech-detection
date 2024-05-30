"""
Module: arguments.py

Handles command line arguments.
"""

import argparse as _argparse
from sys import stdout as _stdout

from loguru import logger as _logger

# Public objects
__all__: list[str] = [
    # VSCode: Sort lines in descending order
    "get_train_arguments",
]


def _configure_logging_level(
    verbose: bool,
) -> None:
    """
    Set the logging level based on the verbose flag.

    Args:
        verbose (bool): Flag to enable verbose logging. If True, set the log level to DEBUG, otherwise, set it to INFO.
    """
    if not verbose:
        _logger.remove()
        _logger.add(_stdout, level="INFO")


def get_train_arguments() -> _argparse.Namespace:
    """
    Get the arguments from the command line for training the model.

    If the verbose flag is not provided, set log level to "INFO", otherwise, keep it as "DEBUG" (default).

    Raises:
        ValueError: If the config file does not end with ".toml" file extension.

    Returns:
        Namespace: Namespace containing the parsed arguments.
    """
    # Initialize argument parser with description and arguments
    parser: _argparse.ArgumentParser = _argparse.ArgumentParser(
        description="train the model"
    )

    # Get mandatory configuration file name from the command line (e.g., bert.toml)
    parser.add_argument(
        "config",
        help="name of the configuration file to use (e.g., 'bert.toml')",
    )

    # Get optional verbose flag from the command line (e.g., --verbose)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="flag to enable verbose logging",
        default=False,
    )

    # Parse the arguments
    args: _argparse.Namespace = parser.parse_args()

    # Raise if the config file does not end with ".toml" file extension
    if not args.config.endswith(".toml"):
        raise ValueError(
            f"Config name must end with '.toml' (e.g., 'bert.toml'): {args.config}",
        )

    # If the verbose flag is not provided, set log level to INFO, otherwise, keep it as DEBUG (default)
    _configure_logging_level(args.verbose)

    return args
