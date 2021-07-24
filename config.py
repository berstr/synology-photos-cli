import logging
import os

# Constants
SYNOLOGY_PHOTO_SHARE = '/photo'

LOGGER = None

# env variables
SYNOLOGY_PHOTO_SERVICE=None
SYNOLOGY_FILESTATION_SERVICE=None


# ==========================
# Init of variables
# ==========================


# SYNOLOGY_FILESTATION_SERVICE is the hostname (IP address) and port number where the plex-rest service runs
SYNOLOGY_FILESTATION_SERVICE=os.environ.get("SYNOLOGY_FILESTATION_SERVICE")
if (SYNOLOGY_FILESTATION_SERVICE == None):
    SYNOLOGY_FILESTATION_SERVICE='localhost:37081'

# SYNOLOGY_PHOTO_SERVICE is the hostname (IP address) and port number where the plex-rest service runs
SYNOLOGY_PHOTO_SERVICE=os.environ.get("SYNOLOGY_PHOTO_SERVICE")
if (SYNOLOGY_PHOTO_SERVICE == None):
    SYNOLOGY_PHOTO_SERVICE='localhost:37083'

def init():
    init_logger()

def init_logger():
    global LOGGER
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(console_handler)

    LOGGER = logger
