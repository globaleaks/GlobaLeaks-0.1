from __future__ import with_statement

from gluon.storage import Storage

import ConfigParser
import os.path

# XXX: find a better place for gleaks.conf ;  $HOME if installed
projroot = os.path.abspath(__file__).rsplit('GlobaLeaks', 1)[0] + 'GlobaLeaks'
cfgfile = os.path.join(projroot, 'globaleaks', 'globaleaks.conf')

def copyform(form, settings):
    """Copy each form value into the specific settings subsection. """
    for name, value in form.iteritems():
        setattr(settings, name, value)
    settings.commit()

class ConfigFile(Storage):
    """
    A Storage-like class which loads and store each attribute into a portable
    conf file.
    """

    def __init__(self, cfgfile, section):
        super(ConfigFile, self).__init__()

        self._cfgfile = cfgfile
        # setting up confgiparser
        self._cfgparser = ConfigParser.ConfigParser()
        self._cfgparser.read([self._cfgfile])
        self._section = section

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__.get(name, None)

        try:
            value = self._cfgparser.get(self._section, name)
            if value.isdigit():
                return int(value)
            elif value.lower() in ('true', 'false'):
                return value.lower() == 'true'
            else:
                return value
        except ConfigParser.NoOptionError:
            return ''  # if option doesn't exists return an empty string

    def __setattr__(self, name, value):
        # keep an open port with private attributes
        if name.startswith('_'):
            self.__dict__[name] = value
            return

        try:
            # XXX: Automagically discover variable type
            self._cfgparser.set(self._section, name, value)
        except ConfigParser.NoOptionError:
            raise NameError(name)

    def commit(self):
        """
        Commit changes in config file.
        """
        with open(self._cfgfile, 'w') as cfgfile:
            self._cfgparser.write(cfgfile)
