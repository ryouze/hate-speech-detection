"""
Script: unpack_datasets.py

Unpacks the BAN-PL `.zip` files into the `datasets` directory as CSV files.

**Note**: Before running this script, make sure to download the BAN-PL dataset by running 'git submodule update --init --recursive'.
"""

from pathlib import Path

from lib import disk, filepaths, utils
from loguru import logger


@logger.catch  # Add pretty exceptions
def main() -> None:
    # Initialize logger with a timestamped log file
    utils.create_timestamped_log_file(__file__, filepaths.logs)

    # Define the input directory containing the BAN-PL dataset `.zip` files
    input_directory: Path = filepaths.modules / "BAN-PL" / "data"

    # Unpack the first version of the dataset (BAN-PL_1.zip)
    # - Upload Date: 16.08.2023
    # - Rows: 24,000
    # - Classes: 0 – non-harmful, 1 – harmful
    logger.info("Unpacking the first version of the dataset...")
    disk.unpack_and_rename(
        zip_file=input_directory / "BAN-PL_1.zip",
        password="BAN-PL_1",
        file_to_extract="BAN-PL.csv",
        output_directory=filepaths.datasets,
        output_file_name="BAN-PL_1.csv",
    )

    # Unpack the second version of the dataset (BAN-PL_2.zip)
    # - Upload Date: 05.04.2023
    # - Rows: 24,000
    # - Classes: 0 – non-harmful, 1 – harmful
    # - Moderation reasons: 4 pseudonymized classes representing moderation reasons
    logger.info("Unpacking the second version of the dataset...")
    disk.unpack_and_rename(
        zip_file=input_directory / "BAN-PL_2.zip",
        password="BAN-PL_2",
        file_to_extract="BAN-PL.csv",
        output_directory=filepaths.datasets,
        output_file_name="BAN-PL_2.csv",
    )

    logger.success("All tasks successfully completed")


if __name__ == "__main__":
    main()
