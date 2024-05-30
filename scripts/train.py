"""
Script: train.py

Trains a transformer-based model (e.g., BERT, DistilBERT, RoBERTa, etc.) on the BAN-PL dataset.

**Note**: Before running this script, make sure to unpack the BAN-PL dataset by running the "unpack_datasets.py" script.
"""

from argparse import Namespace
from typing import Any

from lib import arguments, configurator, filepaths, utils
from loguru import logger

import datasets


@logger.catch  # Add pretty exceptions
def main() -> None:
    # Get the arguments from the command line
    args: Namespace = arguments.get_train_arguments()

    # Initialize logger with a timestamped log file
    utils.create_timestamped_log_file(__file__, filepaths.logs)

    # Load the configuration file from "root/configs" directory using the argument provided (e.g., "bert.toml")
    config: dict[str, Any] = configurator.load_config(
        default_file_path=str(filepaths.configs / "default.toml"),
        custom_file_path=str(filepaths.configs / args.config),
    )
    logger.info(f"Configuration file loaded: {config}")

    # Load the dataset
    path_to_dataset: str = str(filepaths.datasets / config["dataset"])
    logger.info(f"Loading dataset from: {path_to_dataset}")
    dataset: datasets.dataset_dict.DatasetDict = datasets.load_dataset(  # type: ignore
        "csv",
        data_files=path_to_dataset,
    )
    print(dataset)

    logger.success("All tasks successfully completed")


if __name__ == "__main__":
    main()
