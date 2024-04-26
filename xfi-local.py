import subprocess
import argparse
import requests
import time
from xfi.setup import setup
from xfi.extractor_downloader import download_all_extractors, download_local_extractors
from xfi.script_runner import run_bash_script, run_default_scripts
from xfi.supervisord_conf_generator import generate_supervisord_conf
from xfi.indexify_config_generator import create_indexify_config
from xfi.templates import load_templates
from xfi.new_local import NewLocal

def main():
    parser = argparse.ArgumentParser(description="Extractor Downloader")
    parser.add_argument("--all-extractors", action="store_true", help="Download all extractors from the default GitHub URL")
    parser.add_argument("--local-extractors", action="store_true", help="Download extractors from the default local JSON file (local_extractors.json)")
    parser.add_argument("--start", metavar="SCRIPT", nargs="?", const=True, help="Path to the bash script to execute (default: run start_env and start_xfi)")
    parser.add_argument("--setup", action="store_true", help="Run the setup process (get_latest.sh and download all_extractors.json)")
    parser.add_argument("--make-conf", action="store_true", help="Generate supervisord.conf based on local-extractors.json")
    parser.add_argument("--make-init-config", action="store_true", help="Generate indexify.init.config based on the template")
    parser.add_argument("--new-local", metavar="RECIPE_PATH", help="Path to the new_recipe.json file")
    args = parser.parse_args()

    if args.setup:
        setup()
    elif args.all_extractors:
        download_all_extractors()
    elif args.local_extractors:
        download_local_extractors()
    elif args.new_local:
        new_local = NewLocal(args.new_local)
        templates = load_templates()
        new_local.update_configs(templates, input_file=args.new_local)        
        kill_server = f"./utils/kill"
        subprocess.run(kill_server, shell=True, check=True)
        start_server = f"./start_xfi"
        subprocess.Popen(start_server, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Poll the URL until it becomes available
        print("Checking Server Connection")
        while True:
            try:
                response = requests.get("http://localhost:3000/ui/default")
                if response.status_code == 200:
                    break  # URL is available, exit the loop
            except requests.ConnectionError as e:
                # print(f"Polling error: {str(e)}")
                print(" .")
                pass  # URL is not available yet, continue polling
            
            time.sleep(1)  # Wait for 1 second before checking again
        
        new_local.generate_policy()
    elif args.start:
        if args.start is True:
            run_default_scripts()
        else:
            bash_script_path = args.start
            run_bash_script(bash_script_path)
    elif args.make_conf:
        templates = load_templates()
        input_file = "indexify-local/extractors-json/local_extractors.json"
        generate_supervisord_conf(
            input_file=input_file,
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

if __name__ == "__main__":
    main()