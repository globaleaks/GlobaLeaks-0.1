import sys
import random
import string
from fabric.api import run, env, put, get
try:
    import pystache
except:
    print "Pystache not installed. I will not create apache configs!"

class FakeSecHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[asection]\n'
    def readline(self):
        if self.sechead:
            try: return self.sechead
            finally: self.sechead = None
        else: return self.fp.readline()

env.use_ssh_config = True
instance_dir = "/data/globaleaks-instances"

def _make_tor2web_template():
    tor2web_template = 'tor2web/apache2/tor2web'
    f = open(tor2web_template)
    template = ''.join(f.readlines())
    f.close()
    return template

def list_instances():
    print "[+] Listing existing instances..."
    output = run('ls '+instance_dir)
    files = output.split()
    instances = []
    for f in files:
        if f.startswith('demo'):
            instances.append(f)

        if not f.startswith('template'):
            print "    * %s" % f

    instances.sort()
    return instances

def new_instance():
    print "[+] Creating a new instance"
    instances = list_instances()
    # Create the correct template
    idx = instances[-1].replace('demo','')
    if idx == '':
        print "[+] Creating the first new instance!"
        new_instance_idx = '1'
    else:
        new_instance_idx = str(int(idx) + 1)
    new_instance = 'demo'+'0'*(3 - len(new_instance_idx))+new_instance_idx
    template = _make_tor2web_template()

    # Check if template exists
    if not run('ls '+instance_dir+'/template'):
        print "[!] No Template found!"
        print "[+] Cloning globaleaks repo...."
        run('git clone https://github.com/globaleaks/GlobaLeaks.git'+
                                                    instance_dir+'/template')

    # Create copy of globaleaks
    print "[+] Creating copy of globaleaks template..."
    run('cp -R '+instance_dir+'/template '+instance_dir+'/'+new_instance)

    # Fill in the tor2web template
    print "[+] Creating tor2web template..."
    server_name = new_instance+'.globaleaks.org'
    port_number = str(8010 + int(new_instance_idx))
    tor2web_config = {'port_number': '80',
                  'ssl_engine': 'Off',
                  'path_to_sslcertificate': '',
                  'path_to_certificate_key': '',
                  'server_name': server_name,
                  'rewrite_condition': server_name.replace('.', '\\.'),
                  'rewrite_host': env.host+':'+port_number,
                  'dot_onion': ''
                  }
    tor2web_conf_template = pystache.render(template, tor2web_config)
    random_filename = '/tmp/'
    random_filename += ''.join(random.choice(string.ascii_lowercase)
                               for x in range(30))
    with open(random_filename, 'w+') as f:
        f.write(tor2web_conf_template)

    # Push the template to the server
    print "[+] Pushing template to server..."
    put(random_filename,
        '/etc/apache2/sites-enabled/'+new_instance+'-globaleaks')

    print "[+] Getting remote config file..."
    get('/etc/glinstances.conf', random_filename+'.cfg')
    with open(random_filename+'.cfg', 'r') as f:
        import ConfigParser
        config = ConfigParser.SafeConfigParser()
        config.readfp(FakeSecHead(f))
        r_instances = None
        for item, value in config.items('asection'):
            if item == 'instances':
                r_instances = value

    with open(random_filename+'.cfg', 'w+') as f:
        f.write('# THIS WAS SELF GENERATED\n')
        f.write('instance_dir='+instance_dir+'\n')
        if not r_instances:
            f.write('instances='+new_instance+':'+port_number+'\n')
        else:
            f.write('instances='+r_instances+','+new_instance+':'+port_number+'\n')

    put(random_filename+'.cfg', '/etc/glinstances.conf')

    # XXX
    # Create the config file that looks something like this:
    # instance_dir = {{instance_dir}}
    # instances = {{old_instances}},{{new_instance}}:{{port_number}}

