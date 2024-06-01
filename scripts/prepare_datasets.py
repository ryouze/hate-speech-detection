"""
Script: prepare_datasets.py

Unpacks the BAN-PL `.zip` files into the "datasets" directory as CSV files, then sanitizes them.

**Note**: Before running this script, make sure to download the BAN-PL dataset by running 'git submodule update --init --recursive'.
"""

from pathlib import Path

import pandas
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

    # Sanitize the dataset and overwrite the original file (+ rename the columns)
    sanitize_ban1(filepaths.datasets / "BAN-PL_1.csv")

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

    # Sanitize the dataset and overwrite the original file (+ rename the columns)
    sanitize_ban2(filepaths.datasets / "BAN-PL_2.csv")

    logger.success("All tasks successfully completed")


def sanitize_ban1(
    csv_path: Path,
) -> None:
    """
    Sanitize the BAN-PL_1 dataset by removing the "id" column and cleaning the "Text" column. Finally, the "Text" and "Class" columns are renamed to "text" and "labels".

    Args:
        csv_path (Path): Path to the BAN-PL_1 dataset CSV file. It will be modified in-place.
    """
    # Load the dataset
    df: pandas.DataFrame = pandas.read_csv(csv_path)  # type: ignore

    # Drop the "id" column (it contains "###" in some rows, which breaks the conversion to numeric)
    df.drop(columns=["id"], inplace=True)

    # Remove newlines and trailing whitespaces
    df["Text"] = df["Text"].str.replace("\n", " ").str.strip()  # type: ignore

    # Rename the columns (required by the Hugging Face library)
    df.rename(
        columns={
            # from : to
            "Text": "text",
            "Class": "labels",
        },
        inplace=True,
    )

    # Save to disk
    df.to_csv(csv_path, index=False)  # type: ignore


def sanitize_ban2(
    csv_path: Path,
) -> None:
    """
    Sanitize the BAN-PL_2 dataset by removing the "Unnamed: 0" and "id" columns, and cleaning the "Text" column. Finally, the "Text", "Class" and "Reason" columns are renamed to "text", "labels" and "reason".

    Args:
        csv_path (Path): Path to the BAN-PL_2 dataset CSV file. It will be modified in-place.
    """
    # Load the dataset
    df: pandas.DataFrame = pandas.read_csv(csv_path)  # type: ignore

    # Drop the "Unnamed: 0" and "id" columns ("id" contains "###" in some rows, which breaks the conversion to numeric)
    df.drop(columns=["Unnamed: 0", "id"], inplace=True)

    # Remove newlines and trailing whitespaces
    df["Text"] = df["Text"].str.replace("\n", " ").str.strip()  # type: ignore

    # Rename the columns (required by the Hugging Face library)
    df.rename(
        columns={
            # from : to
            "Text": "text",
            "Class": "labels",
            "Reason": "reason",
        },
        inplace=True,
    )

    # Save to disk
    df.to_csv(csv_path, index=False)  # type: ignore


if __name__ == "__main__":
    main()
