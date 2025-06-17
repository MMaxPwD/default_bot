import logging
from logging import getLogger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("aiogram")
logger.setLevel(logging.INFO)

logger = getLogger()
