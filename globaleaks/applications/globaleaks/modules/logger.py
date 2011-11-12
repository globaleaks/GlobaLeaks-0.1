""" This module handles logging on globaleaks."""

import logging, os


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


levels = dict(debug = logging.DEBUG,
              info = logging.INFO,
              warning = logging.WARNING,
              error = logging.ERROR,
              fatal = logging.FATAL,
              client = GLogger.CLIENT,
              server = GLogger.SERVER)


def start_logger(logsettings):
    """
    Start a new logger, set formatting options, and tune level according to use
    configuration.
    """
    logger = logging.getLogger('')
    if logger.handlers:
        if not logsettings.logfile or logsettings.logfile == "disabled":
            logdest = os.devnull
        else:
            logdest = logsettings.logfile

        hdlr = GLogger(logdest)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

        level = levels.get(logsettings.level, None)
        if not level:
            level = levels['fatal']
            logger.waring('Invalid level in config file: set [fatal] as default')

        logger.setLevel(level)

    return logger

