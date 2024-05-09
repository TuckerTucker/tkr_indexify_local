import os
import logging
from typing import Optional
from xfi.local_logger import configure_logging

# Configure logging
configure_logging()

def create_indexify_config(template_file: str, output_file: str) -> None:
    """
    Generate the Indexify configuration file based on the provided template.

    Args:
        template_file (str): Path to the template file.
        output_file (str): Path to save the generated configuration file.
    """
    logging.info(f"Starting to create Indexify configuration from template: {template_file}")
    try:
        # Read the template file
        with open(template_file, 'r') as file:
            template_content = file.read()

        # Get the full path of the destination directory's parent directory
        destination_dir = os.path.dirname(os.path.abspath(os.path.dirname(output_file)))

        # Replace the '../' placeholders with the full path of the destination directory's parent directory
        updated_content = template_content.replace('../', f"{destination_dir}/")

        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write the updated content to the output file
        with open(output_file, 'w') as file:
            file.write(updated_content)

        logging.info(f"Indexify configuration file created at: {output_file}")
    except FileNotFoundError as e:
        logging.error(f"Template file not found: {template_file}")
        logging.exception(e)
    except IOError as e:
        logging.error(f"Error writing to file: {output_file}")
        logging.exception(e)
    except Exception as e:
        logging.error("An unexpected error occurred while creating the Indexify configuration.")
        logging.exception(e)

# Example usage
if __name__ == "__main__":
    create_indexify_config("path/to/template_file.txt", "path/to/output_file.txt")