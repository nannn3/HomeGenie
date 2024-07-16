import json
import logging

def load_json_config(file_path):
    """
    Load a JSON configuration file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data if successful, None otherwise.
    """
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        print("Error: Configuration file not found.")
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in file {file_path}: {e}")
        print("Error: Failed to decode JSON configuration.")
    except IOError as e:
        logging.error(f"I/O error when accessing file {file_path}: {e}")
        print("Error: Unable to access configuration file.")
    return None
