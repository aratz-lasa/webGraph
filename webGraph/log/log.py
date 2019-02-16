import logging
import os


main_logger = logging.getLogger(os.path.basename(os.getcwd()))
db_logger = logging.getLogger("db")