""" This module handles logging on globaleaks."""

import logging


class GLogger(logging.FileHandler):
    """
    Class GLogger provides two more logging options, secifically designed for
    client and server, so that the final user will be able to tune those ones
    in order to avoid leaks of undesidered information.
    """
    # Add two integers to identify server and client log severity.
    CLIENT = 10    # logging.NOTSET==0 < Glogger.CLIENT < Glogger.SERVER
    SERVER = 20    # GLogger.SERVER < logging.info

    def client(self, msg, *args, **kwargs):
        """
        Return a logging message with CLIENT level.
        """
        return log(self.CLIENT, msg, *args, **kwargs)

    def server(self, msg, *args, **kwargs):
        """
        Return a logging message with SERVER level.
        """
        return log(self.SERVER, msg, *args, **kwargs)


def start_logger(logsettings):
    """
    Start a new logger, set formatting options, and tune level according to use
    configuration.
    """
    logger = logging.getLogger()
    if logger.handlers:
        hdlr = GLogger(logsettings.logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

        if logsettings.server:
            logger.setLevel(GLogger.SERVER)
        elif logsettings.client:
            logger.setLevel(GLogger.CLIENT)
        else:
            logger.setLevel(logging.NOTSET)

    return logger
