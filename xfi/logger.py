import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('_local_data/xfi-local.log'),
            logging.StreamHandler()
        ]
    )