import subprocess
from xfi.extractor_downloader import download_all_extractors

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