import os
import logging
from datetime import datetime

log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)

date_str = datetime.now().strftime("%Y-%m-%d")
log_filename = f"debug_{date_str}.log"

logger = logging.getLogger("ElyriaLogger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_directory, log_filename))
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
