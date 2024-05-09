import json
import os
import logging
from typing import List, Dict, Any
from .local_logger import configure_logging

# Configure logging
configure_logging()

def generate_supervisord_conf(input_file: str, output_file: str, template_file: str, chain_name: str = 'default_chain') -> None:
    """
    Generate a supervisord configuration file from a template.

    Args:
        input_file (str): Path to the JSON file containing extractor information.
        output_file (str): Path where the supervisord configuration file will be saved.
        template_file (str): Path to the supervisord template file.
        chain_name (str): Name of the chain to be used in the supervisord configuration.
    """
    logging.info("Starting to generate supervisord configuration file.")
    logging.info(f"Using files: Input={input_file}, Output={output_file}, Template={template_file}")
    try:
        with open(input_file, "r") as file:
            extractors: List[Dict[str, Any]] = json.load(file)

        extractor_programs = ""
        for extractor in extractors:
            module_name = extractor["module_name"]
            module = module_name.split(".")[0]
            extractor_programs += f"""
            [program:{chain_name}-{module}]
            command=indexify-extractor join-server {module_name} --coordinator-addr localhost:8950 --ingestion-addr localhost:8900
            autostart=true
            autorestart=true
            stderr_logfile=_local_data/supervisor/logs/{chain_name}-{module}.err.log
            stdout_logfile=_local_data/supervisor/logs/{chain_name}-{module}.out.log
            priority=3
            """

        with open(template_file, "r") as file:
            template = file.read()

        supervisord_conf = template.replace("{extractor_programs}", extractor_programs.strip())

        # Ensure the directory exists
        output_dir = os.path.dirname(output_file) or '.'
        os.makedirs(output_dir, exist_ok=True)

        with open(output_file, "w") as file:
            file.write(supervisord_conf)

        logging.info(f"Generated supervisord.conf at {output_file}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON data: {e}")
        print(f"Error parsing JSON data: {e}")
    except IOError as e:
        logging.error(f"Error writing to file: {e}")
        print(f"Error writing to file: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")

# Example usage:
# generate_supervisord_conf('input.json', 'output.conf', 'template.conf')