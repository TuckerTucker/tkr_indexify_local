import subprocess
import logging
from typing import List
from .local_logger import configure_logging

# Configure logging
configure_logging()

def run_bash_script(script_path: str) -> None:
    """
    Run the specified bash script using subprocess.

    Args:
        script_path (str): Path to the bash script.

    Raises:
        subprocess.CalledProcessError: If there's an error executing the bash script.
    """
    try:
        # Run the bash script using subprocess
        subprocess.run(["bash", script_path], check=True)
        logging.info(f"Bash script executed successfully: {script_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing bash script: {script_path}")
        logging.exception(e)

def run_default_scripts() -> None:
    """
    Run the default bash scripts specified in the `default_scripts` list.
    """
    default_scripts: List[str] = ["start_xfi"]
    for script in default_scripts:
        run_bash_script(script)

# Example usage:
if __name__ == "__main__":
    try:
        run_default_scripts()
    except Exception as e:
        logging.error("An unexpected error occurred while running default scripts.")
        logging.exception(e)