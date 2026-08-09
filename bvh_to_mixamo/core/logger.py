import logging

LOGGER = logging.getLogger("bvh_to_mixamo")
PREFIX = "[BVH Motion Retargeter]"

if not LOGGER.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False


def log_info(message):
    LOGGER.info("%s %s", PREFIX, message)


def log_warning(message):
    LOGGER.warning("%s %s", PREFIX, message)


def log_error(message):
    LOGGER.error("%s %s", PREFIX, message)
