"""
    .
"""

from includes.logic import ImageLoader
from includes.util.Logging import Logger

logger:Logger = Logger('PreProcessor')

def pre_application():
    logger.debug("Pre Application")

def after_window_init():
    logger.debug("After Window Init")
    ImageLoader.load_fallback_images()
