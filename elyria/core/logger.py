import os
import logging

log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)

logger = logging.getLogger("ElyriaLogger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_directory, "debug.log"))
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
