import argparse
from xfi.extractor_downloader import download_all_extractors, download_local_extractors
from xfi.script_runner import run_bash_script, run_default_scripts
from xfi.setup import setup
from xfi.supervisord_conf_generator import generate_supervisord_conf
from xfi.indexify_config_generator import create_indexify_config

def main():
    parser = argparse.ArgumentParser(description="Extractor Downloader")
    parser.add_argument("--all-extractors", action="store_true", help="Download all extractors from the default GitHub URL")
    parser.add_argument("--local-extractors", action="store_true", help="Download extractors from the default local JSON file (local_extractors.json)")
    parser.add_argument("--start", metavar="SCRIPT", nargs="?", const=True, help="Path to the bash script to execute (default: run start_env and start_xfi)")
    parser.add_argument("--setup", action="store_true", help="Run the setup process (get_latest.sh and download all_extractors.json)")
    parser.add_argument("--make-conf", action="store_true", help="Generate supervisord.conf based on local-extractors.json")
    parser.add_argument("--make-init-config", action="store_true", help="Generate indexify.init.config based on the template")
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
        input_file = "indexify-local/extractors-json/local_extractors.json"
        template_path = 'templates/supervisord.conf.template'
        output_path = 'supervisord.conf'
        generate_supervisord_conf(input_file, output_path, template_path)
    elif args.make_init_config:
        template_path = 'templates/indexify.init.config.template'
        output_path = 'indexify-local/indexify.init.config'
        create_indexify_config(template_path, output_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()