import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import mimetypes
from mime_types import MimeTypes
import logging
from indexify import IndexifyClient
from local_logger import configure_logging

# Set up logging
configure_logging()

class IndexifyClient:
    def upload_file(self, path: str) -> None:
        # Simulate file upload
        logging.info(f"Simulated upload of {path}")

def on_new_file(path: str) -> None:
    """Function to run when a new file is added, checks MIME type and uploads if appropriate."""
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type in MimeTypes.MIMES:
        logging.info(f"Processing and uploading file: {path}")
        try:
            client = IndexifyClient()
            client.upload_file(path=path)
            logging.info(f"File uploaded successfully: {path}")
        except Exception as e:
            logging.error(f"Failed to upload file: {path}. Error: {e}")
    else:
        logging.info(f"Skipped file (unsupported MIME type): {path}")

class Watcher:
    def __init__(self, directory_to_watch: str) -> None:
        self.observer = Observer()
        self.directory_to_watch = directory_to_watch

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
            logging.info("Stopped watching directory")
        except Exception as e:
            logging.error(f"Error: {e}")
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event) -> None:
        if not event.is_directory:
            on_new_file(event.src_path)

if __name__ == "__main__":
    path = "/path/to/watch/directory"
    w = Watcher(path)
    w.run()