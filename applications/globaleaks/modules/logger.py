import logging

def get_logger(settings):
    logger = logging.getLogger()
    if logger.handlers:
        hdlr = logging.FileHandler(settings.logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)
    return logger
