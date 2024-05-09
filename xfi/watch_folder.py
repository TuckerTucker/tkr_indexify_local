import os
import time
import mimetypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from indexify import IndexifyClient
from mime_types import MimeTypes
import logging
from xfi.local_logger import configure_logging


# Configure logging
configure_logging()

class FileHandler(FileSystemEventHandler):
    def on_created(self, event) -> None:
        """
        Handle the event when a file or directory is created.
        """
        logging.info(f"Event detected: {event.src_path}")
        if event.is_directory:
            logging.info(f"Directory created: {event.src_path}")
            self.process_directory(event.src_path)
        else:
            logging.info(f"File created: {event.src_path}")
            self.process_file(event.src_path)

    def process_directory(self, directory_path: str) -> None:
        """
        Process each file in a newly created directory.
        """
        logging.info(f"Processing directory: {directory_path}")
        try:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)
        except Exception as e:
            logging.error(f"Error processing directory: {directory_path}")
            logging.exception(e)

    def process_file(self, file_path: str) -> None:
        """
        Process a file if it matches the MIME types specified in MimeTypes.
        """
        logging.info(f"Processing file: {file_path}")
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type in MimeTypes.MIMES:
                logging.info(f"Accepted MIME type: {mime_type} for file: {file_path}")
                client = IndexifyClient()
                client.upload_file(path=file_path)
            else:
                logging.warning(f"Unsupported MIME type: {mime_type} for file: {file_path}")
        except Exception as e:
            logging.error(f"Error processing file: {file_path}")
            logging.exception(e)

def watch_folder(folder_path: str) -> None:
    """
    Monitor a folder for any new files or directories.
    """
    logging.info(f"Starting to watch folder: {folder_path}")
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Folder watching stopped by user.")
    except Exception as e:
        logging.error(f"Error in folder watching: {folder_path}")
        logging.exception(e)
    finally:
        observer.join()

# Specify the folder path to watch
folder_to_watch = "_watch_folder"

# Start watching the folder
try:
    watch_folder(folder_to_watch)
except Exception as e:
    logging.error(f"Error starting folder watching: {folder_to_watch}")
    logging.exception(e)