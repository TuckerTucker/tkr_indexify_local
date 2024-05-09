import json
import os
import logging
from xfi.local_logger import configure_logging

# Configure logging
configure_logging()

def load_templates(templates_path: str = "templates/templates.json") -> dict:
    """
    Load templates from a JSON file.

    Args:
        templates_path (str): Path to the JSON file containing templates.

    Returns:
        dict: A dictionary containing the loaded templates.

    Raises:
        FileNotFoundError: If the templates file does not exist.
        json.JSONDecodeError: If there is an error parsing the JSON file.
        Exception: For any other unexpected errors.
    """
    logging.info(f"Attempting to load templates from {templates_path}")
    try:
        if not os.path.exists(templates_path):
            logging.error(f"Templates file not found at {templates_path}")
            raise FileNotFoundError(f"Templates file not found at {templates_path}")

        with open(templates_path, 'r') as file:
            templates = json.load(file)
            logging.info("Templates loaded successfully")
            return templates

    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON data from {templates_path}: {e}")
        raise json.JSONDecodeError(f"Error parsing JSON data from {templates_path}: {e}")

    except Exception as e:
        logging.error(f"An unexpected error occurred while loading templates: {str(e)}")
        raise Exception(f"An unexpected error occurred while loading templates: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        templates = load_templates()
        print("Loaded templates:", templates)
    except Exception as e:
        print(f"Failed to load templates: {e}")