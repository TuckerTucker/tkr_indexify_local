import subprocess
import logging
from typing import NoReturn
from .extractor_downloader import download_all_extractors
from .local_logger import configure_logging

# Configure logging
configure_logging()

def setup() -> NoReturn:
    """
    Run the indexify-local/get_latest script and download the all_extractors.json file.
    """
    try:
        # Run the get_latest script using subprocess with the specified working directory
        subprocess.run(["bash", "get_latest"], cwd="indexify-local", check=True)
        logging.info("get_latest script executed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing get_latest script: {e}")
        raise RuntimeError(f"Error executing get_latest script: {e}")

    # Download the all_extractors.json file
    download_all_extractors()

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