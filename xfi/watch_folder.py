import os
import time
import mimetypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from indexify import IndexifyClient
from mime_types import MimeTypes
from logger import configure_logging
import logging, logger

# Configure logging
configure_logging()

class FileHandler(FileSystemEventHandler):
    logging.info("Starting: FileHandler")
    def on_created(self, event):
        try:
            if event.is_directory:
                logging.info(f"Processing: Directory {event.src_path}")
                self.process_directory(event.src_path)
            else:
                logging.info(f"Processing: File {event.src_path}")
                self.process_file(event.src_path)
        except Exception as e:
            logging.error(f"Error processing event: {event}")
            logging.exception(e)  # Log the full exception traceback    

    def process_directory(self, directory_path):
        try:
            logging.info(f"New directory detected: {directory_path}")
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)
        except Exception as e:
            logging.error(f"Error processing directory: {directory_path}")
            logging.exception(e)

    def process_file(self, file_path):
        try:
            file_directory, file_name = os.path.split(file_path)
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            mime_type, _ = mimetypes.guess_type(file_path)

            if mime_type in MimeTypes.MIMES:
                logging.info(f"Processing file: {file_name}")
                logging.info(f"File size: {file_size_mb:.2f} MB")
                logging.info(f"File type: {mime_type}")

                client = IndexifyClient()
                client.upload_file(path=file_path)
            else:
                logging.warning(f"Skipping {file_name} (MIME type: {mime_type})")

        except Exception as e:
            logging.error(f"Error processing file: {file_path}")
            logging.exception(e)

def watch_folder(folder_path):
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        print(f"Error in folder watching: {folder_path}")
        print(f"Error details: {str(e)}")
    finally:
        observer.join()

# Specify the folder path to watch
folder_to_watch = "_watch_folder"

# Start watching the folder
try:
    logging.info(f"Watching: Folder {folder_to_watch}")
    watch_folder(folder_to_watch)
except Exception as e:
    print(f"Error starting folder watching: {folder_to_watch}")
    print(f"Error details: {str(e)}")