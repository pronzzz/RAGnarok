import logging

def setup_logger(verbose: bool = False, debug: bool = False) -> logging.Logger:
    """Configure the global logger for RAGnarok."""
    logger = logging.getLogger("ragnarok")

    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    # Prevent adding multiple handlers if setup_logger is called repeatedly
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] %(message)s" if not debug else "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
