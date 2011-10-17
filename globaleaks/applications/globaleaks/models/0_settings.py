import ConfigParser
import os.path

from gluon.storage import Storage
from config import ConfigFile, cfgfile

################################################################
# Import the database and global settings from the config file #
################################################################

settings = Storage()

settings.globals = ConfigFile(cfgfile, 'global')
settings.database = ConfigFile(cfgfile, 'database')

