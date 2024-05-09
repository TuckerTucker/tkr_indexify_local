import json
import logging
from typing import Dict, Any

from indexify import IndexifyClient
from xfi.supervisord_conf_generator import generate_supervisord_conf
from xfi.indexify_config_generator import create_indexify_config
from xfi.local_logger import configure_logging

# Configure logging
configure_logging()

class NewLocal:
    def __init__(self, recipe_path: str) -> None:
        """
        Initialize the NewLocal class with the recipe from the specified path.

        Args:
            recipe_path (str): Path to the recipe JSON file.
        """
        try:
            with open(recipe_path, 'r') as file:
                recipe = json.load(file)
                self.extractors = recipe['extractors']
                self.chain_name = recipe['name']
            logging.info(f"Loaded recipe from {recipe_path}")
        except FileNotFoundError:
            logging.error(f"Recipe file not found: {recipe_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from the recipe file: {recipe_path}")
            raise

    def generate_policy(self) -> None:
        """
        Generate extraction policies for each extractor in the recipe.
        """
        client = IndexifyClient()
        for i, extractor in enumerate(self.extractors):
            module = extractor["module_name"].split(".")[0]
            extractor_name = f"tensorlake/{module}"  # This will need to change when custom extractors are being used

            if i == 0:
                content_source = "ingestion"
            else:
                prev_extractor = self.extractors[i-1]["module_name"].split(".")[0]
                content_source = f"{prev_extractor}-{self.chain_name}"

            client.add_extraction_policy(
                extractor=extractor_name,
                name=f"{module}-{self.chain_name}",
                content_source=content_source
            )
        self.extraction_policies = client.extraction_policies
        logging.info("Extraction policies generated successfully.")

    def update_configs(self, templates: Dict[str, Dict[str, str]], input_file: str) -> None:
        """
        Update configuration files based on the provided templates.

        Args:
            templates (Dict[str, Dict[str, str]]): Dictionary containing template paths and output paths.
            input_file (str): Path to the input JSON file for the supervisord configuration.
        """
        # Update supervisor config
        generate_supervisord_conf(
            input_file=input_file,
            output_file=templates['supervisord']['output_path'],
            template_file=templates['supervisord']['template_path'],
            chain_name=self.chain_name
        )

        # Update indexify config
        create_indexify_config(
            template_file=templates['indexify']['template_path'],
            output_file=templates['indexify']['output_path']
        )
        logging.info("Configuration files updated successfully.")

# Example usage:
# new_local_instance = NewLocal("path_to_recipe.json")
# new_local_instance.generate_policy()
# new_local_instance.update_configs(templates_dict, "input_file.json")