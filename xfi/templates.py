import json

def load_templates(templates_path="templates/templates.json"): 
    with open(templates_path, 'r') as file:
        return json.load(file)