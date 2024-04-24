import argparse
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

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
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
        with open(input_file, "r") as file:
            extractors = json.load(file)
        for extractor in extractors:
            extractor_type = extractor["type"]
            module_name = extractor["module_name"]
            module = module_name.split(".")[0]
            cli_call = f"indexify-extractor download hub://{extractor_type}/{module}"
            try:
                subprocess.run(cli_call, shell=True, check=True)
                print(f"Successfully downloaded extractor: {module_name}")
            except subprocess.CalledProcessError as e:
                print(f"Error downloading extractor {module_name}: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")

def run_bash_script(script_path):
    try:
        # Run the bash script using subprocess
        subprocess.run(["bash", script_path], check=True)
        print(f"Bash script executed successfully: {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash script: {script_path}")
        print(f"Error message: {e}")

def run_default_scripts():
    default_scripts = ["start_xfi"]
    for script in default_scripts:
        run_bash_script(script)

def setup():
    """
    Run the indexify-local/get_latest script and download the all_extractors.json file.
    """
    try:
        
        # Run the get_latest script using subprocess with the specified working directory
        subprocess.run(["bash", "get_latest"], cwd="indexify-local", check=True)
        print("get_latest script executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error executing get_latest script: {e}")

    # Download the all_extractors.json file
    download_all_extractors()
def generate_supervisord_conf(input_file="indexify-local/extractors-json/local_extractors.json", output_file="supervisord.conf"):
    try:
        with open(input_file, "r") as file:
            extractors = json.load(file)

        conf_template = """
            [supervisord]
            nodaemon=true
            logfile=%(ENV__LOCAL_DATA_DIR)s/supervisor/supervisord.log
            pidfile=%(ENV__LOCAL_DATA_DIR)s/supervisor/supervisord.pid
            childlogdir=%(ENV__LOCAL_DATA_DIR)s/supervisor

            [program:indexify_server]
            command=%(ENV_INDEXIFY_LOCAL_DIR)s/indexify server  -d --config-path %(ENV_INDEXIFY_LOCAL_DIR)s/indexify.init.config
            autostart=true
            autorestart=true
            stderr_logfile=%(ENV__LOCAL_DATA_DIR)s/supervisor/logs/indexify_server.err.log
            stdout_logfile=%(ENV__LOCAL_DATA_DIR)s/supervisor/logs/indexify_server.out.log
            priority=1

            [program:watch_folder]
            command=python %(ENV_WATCH_FOLDER_DIR)s/watch_folder.py
            autostart=true
            autorestart=true
            stderr_logfile=%(ENV__LOCAL_DATA_DIR)s/supervisor/logs/watch_folder.err.log
            stdout_logfile=%(ENV__LOCAL_DATA_DIR)s/supervisor/logs/watch_folder.out.log
            priority=2
            """

        for extractor in extractors:
            module_name = extractor["module_name"]
            module = module_name.split(".")[0]
            conf_template += f"""
            [program:{module}]
            command=indexify-extractor join-server {module_name} --coordinator-addr %(ENV_COORDINATOR_ADDR)s --ingestion-addr %(ENV_INGESTION_ADDR)s
            autostart=true
            autorestart=true
            stderr_logfile=%(ENV__LOCAL_DATA_DIR)s/supervisor/logs/{module}.err.log
            stdout_logfile=%(ENV__LOCAL_DATA_DIR)s/supervisor/logs/{module}.out.log
            priority=3
            """

        with open(output_file, "w") as file:
            file.write(conf_template.strip())

        print(f"Generated supervisord.conf at {output_file}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extractor Downloader")
    parser.add_argument("--all-extractors", action="store_true", help="Download all extractors from the default GitHub URL")
    parser.add_argument("--local-extractors", action="store_true", help="Download extractors from the default local JSON file (local_extractors.json)")
    parser.add_argument("--start", metavar="SCRIPT", nargs="?", const=True, help="Path to the bash script to execute (default: run start_env and start_xfi)")
    parser.add_argument("--setup", action="store_true", help="Run the setup process (get_latest.sh and download all_extractors.json)")
    parser.add_argument("--make-conf", action="store_true", help="Generate supervisord.conf based on local-extractors.json")
    args = parser.parse_args()

    if args.setup:
        setup()
    elif args.all_extractors:
        download_all_extractors()
    elif args.local_extractors:
        download_local_extractors()
    elif args.start:
        if args.start is True:
            run_default_scripts()
        else:
            bash_script_path = args.start
            run_bash_script(bash_script_path)
    elif args.make_conf:
        generate_supervisord_conf()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()