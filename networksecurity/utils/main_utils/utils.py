import yaml
import os, sys

import pandas as pd

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    Args:
        file_path (str): Path to the YAML file.
    Returns:
        dict: Content of the YAML file.
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes the given content to a YAML file at the specified file path.
    If the 'replace' flag is set to True and the file already exists, the existing file will be removed
    before writing the new content. The function ensures that the directory structure for the file path exists.
    Args:
        file_path (str): The path where the YAML file will be written.
        content (object): The content to be serialized and written to the YAML file.
        replace (bool, optional): Whether to replace the file if it already exists. Defaults to False.
    Raises:
        NetworkSecurityException: If any error occurs during the file writing process.
    """
    
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)