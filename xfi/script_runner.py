import subprocess

def run_bash_script(script_path):
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
        print(f"Bash script executed successfully: {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash script: {script_path}")
        print(f"Error message: {e}")

def run_default_scripts():
    """
    Run the default bash scripts specified in the `default_scripts` list.
    """
    default_scripts = ["start_xfi"]
    for script in default_scripts:
        run_bash_script(script)