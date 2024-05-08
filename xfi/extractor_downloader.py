import json
import os
import subprocess
import requests
from typing import Optional
import logging

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def download_all_extractors(url: str = None, output_file: str = "indexify-local/extractors-json/all_extractors.json") -> None:
    """
    Download the JSON file containing all extractors from the specified URL
    or the default GitHub URL and save it locally.
    """
    if url is None:
        url = "https://raw.githubusercontent.com/tensorlakeai/indexify-extractors/main/extractors.json"

    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        with open(output_file, "w") as file:
            json.dump(data, file, indent=2)

        logging.info(f"Successfully downloaded all extractors to {output_file}")
        print(f"Successfully downloaded all extractors to {output_file}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading all extractors: {e}")
        print(f"Error downloading all extractors: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON data: {e}")
        print(f"Error parsing JSON data: {e}")
    except IOError as e:
        logging.error(f"Error writing to file: {e}")
        print(f"Error writing to file: {e}")


def update_local_extractors_list(input_file: str, output_file: str = "indexify-local/extractors-json/local_extractors.json") -> None:
    """
    Update the local extractors list by adding new extractors from the input file if they are not already present.
    Adjusted to handle the format of whisper_chain.json.
    """
    logging.info("Starting update of local extractors list")
    try:
        if not os.path.exists(input_file):
            logging.error(f"Input file {input_file} does not exist.")
            print(f"Error: Input file {input_file} does not exist.")
            return

        with open(input_file, "r") as file:
            data = json.load(file)
            new_extractors = data.get("extractors", [])  # Adjusted to handle nested structure
            if not isinstance(new_extractors, list) or not all(isinstance(extractor, dict) for extractor in new_extractors):
                raise ValueError("Input file does not contain a valid list of extractor dictionaries.")

        if not os.path.exists(output_file):
            existing_extractors = []
        else:
            with open(output_file, "r") as file:
                existing_extractors = json.load(file)
                if not isinstance(existing_extractors, list) or not all(isinstance(extractor, dict) for extractor in existing_extractors):
                    existing_extractors = []

        updated = False
        for new_extractor in new_extractors:
            if new_extractor not in existing_extractors:
                existing_extractors.append(new_extractor)
                updated = True

        if updated:
            with open(output_file, "w") as file:
                json.dump(existing_extractors, file, indent=4)
                logging.info(f"Updated local extractors list and written to {output_file}.")
                print(f"Updated local extractors list and written to {output_file}.")
        else:
            logging.info("No updates needed.")
            print("No updates needed.")

    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON data: {e}")
        print(f"Error parsing JSON data: {e}")
    except IOError as e:
        logging.error(f"Error writing to file {output_file}: {e}")
        print(f"Error writing to file {output_file}: {e}")
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        print(f"Validation error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")

def download_extractors(input_file: str) -> None:
    """
    Download extractors specified in the local extractors JSON file and update the list.
    Adjusted to handle the format of whisper_chain.json.
    """
    logging.info("Starting download of extractors")

    if not os.path.exists(input_file):
        logging.error(f"The specified file '{input_file}' does not exist.")
        print(f"Error: The specified file '{input_file}' does not exist.")
        return

    try:
        with open(input_file, "r") as file:
            data = json.load(file)
            extractors = data.get("extractors", [])

        for extractor in extractors:
            if "module_name" not in extractor or "type" not in extractor:
                logging.error("Missing required fields in extractor definition.")
                print("Error: Missing required fields in extractor definition.")
                continue

            module_name = extractor["module_name"]
            module = module_name.split(".")[0]
            extractor_type = extractor["type"]
            cli_call = f"indexify-extractor download hub://{extractor_type}/{module}"

            try:
                subprocess.run(cli_call, shell=True, check=True)
                update_local_extractors_list(input_file)
                logging.info(f"Successfully downloaded extractor: {module_name}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error downloading extractor {module_name}: {e}")
                print(f"Error downloading extractor {module_name}: {e}")

    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON data: {e}")
        print(f"Error parsing JSON data: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")

    logging.info("Completed download of extractors")