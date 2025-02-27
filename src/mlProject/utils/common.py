import os                           # Provides functions for interacting with the operating system
from box.exceptions import BoxValueError  # Exception from the Box library used when a Box value is invalid or missing
import yaml                         # Library for parsing YAML files
from src.mlProject import logger        # Importing the project's custom logger for logging messages
import json                         # Library for JSON serialization and deserialization
import joblib                       # Library for saving and loading Python objects in binary format
from ensure import ensure_annotations  # Decorator to enforce type annotations at runtime
from box import ConfigBox           # ConfigBox wraps dictionaries to allow attribute-style access
from pathlib import Path            # Provides object-oriented filesystem paths
from typing import Any              # Allows for type annotations of any type


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.

    Args:
        path_to_yaml (Path): The path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty.
        Exception: Propagates any other exceptions that occur while reading the file.

    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            # Safely load the YAML file content into a Python dictionary
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            # Wrap the dictionary in a ConfigBox for attribute-style access and return it
            return ConfigBox(content)
    except BoxValueError:
        # Raise an error if the YAML file is empty or invalid
        raise ValueError("yaml file is empty")
    except Exception as e:
        # Propagate any other exceptions
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates a list of directories if they do not exist.

    Args:
        path_to_directories (list): A list of directory paths to be created.
        verbose (bool, optional): If True, logs each directory creation. Defaults to True.
    """
    for path in path_to_directories:
        # Create the directory and any necessary parent directories
        os.makedirs(path, exist_ok=True)
        if verbose:
            # Log the creation of each directory
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves a dictionary as a JSON file at the specified path.

    Args:
        path (Path): The file path where the JSON data will be saved.
        data (dict): The data to be saved in JSON format.
    """
    with open(path, "w") as f:
        # Dump the dictionary to the file with an indentation of 4 for readability
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads JSON data from a file and returns it as a ConfigBox.

    Args:
        path (Path): The file path from where the JSON data will be loaded.

    Returns:
        ConfigBox: The loaded data wrapped in a ConfigBox for attribute-style access.
    """
    with open(path) as f:
        # Load the JSON content from the file into a dictionary
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path}")
    # Wrap the dictionary in a ConfigBox and return it
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Saves any Python object as a binary file using joblib.

    Args:
        data (Any): The Python object to be saved.
        path (Path): The file path where the binary data will be saved.
    """
    # Dump the object to the specified file path
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads a Python object from a binary file.

    Args:
        path (Path): The file path from where the binary data will be loaded.

    Returns:
        Any: The Python object stored in the binary file.
    """
    # Load the object using joblib from the specified file path
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns the size of a file in kilobytes.

    Args:
        path (Path): The file path whose size is to be determined.

    Returns:
        str: A formatted string representing the size of the file in KB.
    """
    # Calculate file size in kilobytes by dividing bytes by 1024 and rounding the result
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"
