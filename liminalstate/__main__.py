from liminalstate.internal.cli.cli import LiminalCLI


import logging
from logging.handlers import RotatingFileHandler

log_file = "wowedits.log"
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_file)
rotating_handling = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
rotating_handling.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])
logger = logging.getLogger(__name__)


def main():
    cli = LiminalCLI()
    cli.cmdloop()
