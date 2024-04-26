import json
from indexify import IndexifyClient
from xfi.supervisord_conf_generator import generate_supervisord_conf
from xfi.indexify_config_generator import create_indexify_config

class NewLocal:
    def __init__(self, recipe_path):
        with open(recipe_path, 'r') as file:
            recipe = json.load(file)
            self.extractors = recipe['extractors']
            self.chain_name = recipe['name']

    def generate_policy(self):
        client = IndexifyClient()
        i=0
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

    def update_configs(self, templates, input_file):
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