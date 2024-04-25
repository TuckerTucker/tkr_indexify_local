import json
import os
import subprocess
import requests

def download_all_extractors(url=None, output_file="indexify-local/extractors-json/all_extractors.json"):
    """
    Download the JSON file containing all extractors from the specified URL
    or the default GitHub URL and save it locally in the indexify-local/extractors-json directory.
    """
    if url is None:
        url = "https://raw.githubusercontent.com/tensorlakeai/indexify-extractors/main/extractors.json"

    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Download the JSON file from the specified URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse the JSON data
        data = response.json()

        # Write the JSON data to the output file
        with open(output_file, "w") as file:
            json.dump(data, file, indent=2)

        print(f"Successfully downloaded all extractors to {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading all extractors: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def download_local_extractors(input_file="indexify-local/extractors-json/local_extractors.json"):
    """
    Open the JSON file named local_extractors.json (or the specified file) from the
    indexify-local/extractors-json directory and download each extractor using the CLI call.
    """
    try:
        # Open the JSON file and load the extractor data
        with open(input_file, "r") as file:
            extractors = json.load(file)

        # Iterate over each extractor and download it using the CLI call
        for extractor in extractors:
            extractor_type = extractor["type"]
            module_name = extractor["module_name"]
            module = module_name.split(".")[0]
            cli_call = f"indexify-extractor download hub://{extractor_type}/{module}"

            try:
                # Run the CLI call using subprocess
                subprocess.run(cli_call, shell=True, check=True)
                print(f"Successfully downloaded extractor: {module_name}")
            except subprocess.CalledProcessError as e:
                print(f"Error downloading extractor {module_name}: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")