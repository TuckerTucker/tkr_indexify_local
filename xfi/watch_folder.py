import time
import os  # Import the os module
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import argparse
from indexify import IndexifyClient
from local_logger import configure_logging

# Set up logging
configure_logging()

class WatchFolder:
    def __init__(self, directory_to_watch: str) -> None:
        self.observer = Observer()
        self.directory_to_watch = os.path.abspath(directory_to_watch)  # Get the absolute path
        logging.info(f"Initialized WatchFolder with directory: {self.directory_to_watch}")

    def run(self) -> None:
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        logging.info(f"Started watching directory: {self.directory_to_watch}")
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            logging.info("Stopped watching directory due to KeyboardInterrupt")
        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)  # Log the full exception information
            self.observer.stop()
        self.observer.join()
        logging.info(f"Stopped watching directory: {self.directory_to_watch}")

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event) -> None:
        if not event.is_directory:
            Handler().on_new_file(event.src_path)  # Call the instance method

    def on_new_file(self, file_path: str) -> None:  # Instance method
        client = IndexifyClient()
        client.upload_file(path=file_path)
        logging.info(f"New file created and uploaded: {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # Create an ArgumentParser object
    parser.add_argument("--directory", help="Directory to be watched", default="_watch_folder")  # Add argument with default value
    args = parser.parse_args()  # Parse the arguments
    w = WatchFolder(args.directory)  # Pass the directory as an argument
    w.run()