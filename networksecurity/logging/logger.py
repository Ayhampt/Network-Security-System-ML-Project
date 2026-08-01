import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%H:%M:%S')}.log"
LOG_SUB_FOLDER = f"{datetime.today().strftime('%m_%d_%Y')}"
logs_path = os.path.join(os.getcwd(), "logs", LOG_SUB_FOLDER)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
