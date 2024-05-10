import subprocess
import logging
import os
from typing import NoReturn
from .extractor_downloader import download_all_extractors, download_extractors
from .local_logger import configure_logging
from .templates import load_templates
from xfi.supervisord_conf_generator import generate_supervisord_conf
from xfi.indexify_config_generator import create_indexify_config

configure_logging()  # Configure logging

def install_requirements() -> None:
    """
    Installs the Python packages specified in the requirements.txt file without using the cache.
    """
    try:
        subprocess.run(['pip', 'install', '--no-cache-dir', '-r', 'requirements.txt'], check=True)
        logging.info("Successfully installed packages from requirements.txt without using cache")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install packages: {e}")
        raise RuntimeError(f"Failed to install packages: {e}")

def setup(chain_file: str = "whisper_chain.json") -> NoReturn:
    """
    Setup the environment by installing dependencies, running scripts, and configuring files.
    
    Args:
        chain_file (str): The filename of the chain file to download. Defaults to "whisper_chain.json".
    """
    # Install required Python packages
    install_requirements()
    
    # Get the list of extractors from indexify github
    download_all_extractors()

    try:
        subprocess.run(["bash", "get_latest"], cwd="indexify-local", check=True)
        logging.info("get_latest script executed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing get_latest script: {e}")
        raise RuntimeError(f"Error executing get_latest script: {e}")
    
    download_extractors(chain_file)
    logging.info(f"Downloaded extractors from {chain_file} successfully")

    templates = load_templates()
    input_file_list = templates['supervisord']['input_file']
    input_file_path = input_file_list
    full_path = os.path.abspath(input_file_path)
    
    generate_supervisord_conf(
        input_file=full_path,
        output_file=templates['supervisord']['output_path'],
        template_file=templates['supervisord']['template_path']
    )

    create_indexify_config(
        template_file=templates['indexify']['template_path'],
        output_file=templates['indexify']['output_path']
    )
    
    try:
        subprocess.run(["bash", "setup_ui"], cwd="utils", check=True)
        logging.info("UI setup successful")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting up UI: {e}")
        raise RuntimeError(f"Error setting up UI: {e}")

def reset() -> NoReturn:
    """
    Clear all logs and config files.
    """
    try:
        subprocess.run(["bash", "reset_local"], cwd="utils", check=True)
        logging.info("reset_local script executed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing reset_local script: {e}")
        raise RuntimeError(f"Error executing reset_local script: {e}")

def clear_logs() -> NoReturn:
    """
    Clear all logs.
    """
    try:
        subprocess.run(["bash", "clear_logs"], cwd="utils", check=True)
        logging.info("clear_logs script executed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing clear_logs script: {e}")
        raise RuntimeError(f"Error executing clear_logs script: {e}")