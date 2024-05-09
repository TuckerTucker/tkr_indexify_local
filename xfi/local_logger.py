import logging.config

def configure_logging():
    """
    Configure logging using the logging.config module to provide advanced logging options.
    """
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'fileHandler': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': '_local_data/xfi-local.log',
                'mode': 'a',
            },
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'INFO',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['fileHandler', 'consoleHandler'],
                'level': 'INFO',
                'propagate': True
            }
        }
    }

    logging.config.dictConfig(LOGGING_CONFIG)

# Example usage:
if __name__ == "__main__":
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Logging is configured.")