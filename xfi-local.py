import argparse
import logging
import os
import subprocess
import requests
import time
from typing import NoReturn
from xfi.setup import setup, reset, clear_logs
from xfi.extractor_downloader import download_all_extractors, download_extractors
from xfi.script_runner import run_bash_script, run_default_scripts
from xfi.supervisord_conf_generator import generate_supervisord_conf
from xfi.indexify_config_generator import create_indexify_config
from xfi.templates import load_templates
from xfi.new_local import NewLocal
from xfi.local_logger import configure_logging

def check_file_exists(file_path: str) -> None:
    """Check if a file exists at the specified path."""
    if not os.path.exists(file_path):
        logging.error(f"We Checked, it doesn't exist: {file_path}")
        raise FileNotFoundError(f"We Checked, it doesn't exist: {file_path}")
    else:
        logging.info(f"Yep, it's there: {file_path}")

def main() -> NoReturn:
    """Main function to parse arguments and handle the program flow based on user input."""
    configure_logging()
    logging.info("Starting main function")

    parser = argparse.ArgumentParser(description="xfi local")
    parser.add_argument("--setup", nargs='?', const='whisper_chain.json', metavar='FILE', help="Run the setup process with the specified file or default to 'whisper_chain.json'")
    parser.add_argument("--reset", action="store_true", help="Removes all logs and config files")
    parser.add_argument("--clear-logs", action="store_true", help="Removes all logs")
    parser.add_argument("--all-extractors", action="store_true", help="Download all extractors from the default GitHub URL")
    parser.add_argument("--local-extractors", metavar="INPUT_FILE", help="Download extractors from the specified JSON file")
    parser.add_argument("--start", metavar="SCRIPT", nargs="?", const=True, help="Path to the bash script to execute (default: run start_env and start_xfi)")
    parser.add_argument("--make-conf", action="store_true", help="Generate supervisord.conf based on local-extractors.json")
    parser.add_argument("--make-init-config", action="store_true", help="Generate indexify.init.config based on the template")
    parser.add_argument("--new-local", metavar="RECIPE_PATH", help="Path to the new_recipe.json file")

    args = parser.parse_args()

    try:
        if args.setup:
            setup(args.setup)
        elif args.reset:
            reset()
        elif args.clear_logs:
            clear_logs()
        elif args.all_extractors:
            download_all_extractors()
        elif args.local_extractors:
            download_extractors(input_file=args.local_extractors)
        elif args.new_local:
            new_local = NewLocal(args.new_local)
            new_local.generate_policy()
            templates = load_templates()
            new_local.update_configs(templates, input_file=args.new_local)
            subprocess.run("./utils/kill", shell=True, check=True)
            subprocess.Popen("./start_xfi", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logging.info("Checking Server Connection")
            while True:
                try:
                    response = requests.get("http://localhost:3000/ui/default")
                    if response.status_code == 200:
                        break
                except requests.ConnectionError as e:
                    logging.debug(f"Polling error: {str(e)}")
                    time.sleep(1)
            new_local.generate_policy()
        elif args.start:
            if args.start is True:
                run_default_scripts()
            else:
                run_bash_script(args.start)
        elif args.make_conf:
            templates = load_templates()
            input_file_list = templates['supervisord']['input_file'],
            input_file_path = input_file_list[0],  # This gets the string 'input_file'
            logging.info(input_file_path)
            full_path = os.path.abspath(input_file_path[0]),
            logging.info(full_path[0])
            check_file_exists(full_path[0])
            generate_supervisord_conf(
                input_file=full_path[0],
                output_file=templates['supervisord']['output_path'],
                template_file=templates['supervisord']['template_path']
            )
        elif args.make_init_config:
            templates = load_templates()
            create_indexify_config(
                template_file=templates['indexify']['template_path'],
                output_file=templates['indexify']['output_path']
            )
        else:
            parser.print_help()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        logging.info("Ending main function")

if __name__ == "__main__":
    main()