import logging

logger = logging.getLogger("assistant_api")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
