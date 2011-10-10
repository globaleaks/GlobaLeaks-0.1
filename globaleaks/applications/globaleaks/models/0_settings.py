import ConfigParser
import os.path

from gluon.storage import Storage
from config import ConfigFile

################################################################
# Import the database and global settings from the config file #
################################################################

cfgfile = os.path.join(os.path.dirname(__file__), 'gleaks.cfg')

settings = Storage()

settings.globals = ConfigFile(cfgfile, 'global')
settings.database = ConfigFile(cfgfile, 'database')

