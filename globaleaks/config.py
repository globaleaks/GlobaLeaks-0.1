from gluon.storage import Storage
from gluon.tools import Auth
import ConfigParser

class ConfigFile(Storage):

    def __init__(self, cfgfile, section):
        super(ConfigFile, self).__init__()

        self._cfgfile = cfgfile
        # setting up confgiparser
        self._cfgparser = ConfigParser.ConfigParser()
        self._cfgparser.read([self._cfgfile])
        #
        self._section = section

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__.get(name, None)

        try:
            return self._cfgparser.get(self._section, name)
        except ConfigParser.NoOptionError:
            raise NameError(name)

    def __setattr__(self, name, value):
        # keep an open port with private attributes
        if name.startswith('_'):
            self.__dict__[name] = value
            return

        try:
            self._cfgparser.set(self._section, name, value)
            self._cfgparser.write(open(self._cfgfile, 'w'))
        except ConfigParser.NoOptionError:
            raise NameError(name)

Auth.commit = lambda self: 0
