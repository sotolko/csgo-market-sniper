import logging


def prepare_buy_log() -> logging.Logger:
    """
    Sets up a logger to record purchase details.

    Returns:
    logger (logging.Logger): A configured logger for recording purchase details.
    """

    # Initialize a logger
    logger = logging.getLogger('BUY')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # If no handlers are configured, set up a file handler
    if not logger.handlers:
        file_handler = logging.FileHandler("buy.log", mode='a')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Return the configured logger
    return logger
