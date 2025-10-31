import sys
from .config import cfg
from .generate_page import process_product_row, generate_page_main
from .filters import create_filters
from .cli import main
from loguru import logger

# set logger level
logger.remove()
logger.add(sys.stderr, level=cfg.LOGGER_LEVEL)
