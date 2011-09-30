import logging

def get_logger(settings):
    logger = logging.getLogger()
    if logger.handlers:
        hdlr = logging.FileHandler(settings.globals.logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        if settings.logging.server and settings.logging.client:
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.INFO)
    return logger
