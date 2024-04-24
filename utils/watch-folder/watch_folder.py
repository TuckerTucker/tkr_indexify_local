import os
import time
import mimetypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from indexify import IndexifyClient
from mime_types import MimeTypes
import logging

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        try:
            if event.is_directory:
                self.process_directory(event.src_path)
            else:
                self.process_file(event.src_path)
        except Exception as e:
            print(f"Error processing event: {event}")
            print(f"Error details: {str(e)}")

    def process_directory(self, directory_path):
        try:
            print(f"\033[96mNew directory detected:\033[0m \n {directory_path}")
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)
            print("\n")
        except Exception as e:
            print(f"Error processing directory: {directory_path}")
            print(f"Error details: {str(e)}")

    def process_file(self, file_path):
        try:
            file_directory, file_name = os.path.split(file_path)
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            # Get the MIME type of the file
            mime_type, _ = mimetypes.guess_type(file_path)

            if mime_type in [mime for mime in MimeTypes.MIMES]:
                logging.info(f"\033[36mProcessing file:\033[0m \n {file_name} \n")
                # print(f"File size: {file_size_mb:.2f} MB")
                # print(f"File type: {mime_type}")
                # print("\n")
                client = IndexifyClient()
                client.upload_file(path=file_path)
            else:
                print(f"\033[33mSkipping {file_name}\033[0m \n (MIME type: {mime_type})")
        except Exception as e:
            print(f"Error processing file: {file_path}")
            print(f"Error details: {str(e)}")

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
folder_to_watch = "../_local_data/_watch_folder"

# Start watching the folder
try:
    watch_folder(folder_to_watch)
except Exception as e:
    print(f"Error starting folder watching: {folder_to_watch}")
    print(f"Error details: {str(e)}")