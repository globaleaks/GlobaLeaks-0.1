from gluon.storage import Storage
class ConfigFile(Storage):

    def __init__(self, cfgparser, section):
        super(ConfigFile, self).__init__()

        self._cfgparser = cfgparser
        self._section = section

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__.get(name, None)
        try:
            return self._cfgparser.get(self._section, name)
        except ConfigParser.NoOptionError:
            raise NameError

    def __setattr__(self, name, value):
        # keep an open port with private attributes
        if name.startswith('_'):
            self.__dict__[name] = value
        try:
            self._cfgparser.set(self._section, name, value)
        except ConfigParser.NoOptionError:
            raise NameError

