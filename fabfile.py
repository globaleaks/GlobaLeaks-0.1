import sys
import random
import string
from fabric.api import run, env, put
try:
    import pystache
except:
    print "Pystache not installed. I will not create apache configs!"

env.use_ssh_config = True
instance_dir = "/data/globaleaks-instances"

def _make_tor2web_template():
    tor2web_template = 'tor2web/apache2/tor2web'
    f = open(tor2web_template)
    template = ''.join(f.readlines())
    f.close()
    return template

def list_instances():
    output = run('ls '+instance_dir)
    files = output.split()
    instances = []
    for f in files:
        if f.startswith('demo'):
            instances.append(f)
    instances.sort()
    return instances

def new_instance():
    instances = list_instances()

    # Create the correct template
    new_instance_idx = str(int(instances[-1].replace('demo','')) + 1)
    new_instance = 'demo'+'0'*(3 - len(new_instance_idx))+new_instance_idx
    template = _make_tor2web_template()

    # Create copy of globaleaks
    run('cp -R '+instance_dir+'/template '+instance_dir+'/demo003')

    # Fill in the tor2web template
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
    put(random_filename,
        '/etc/apache2/sites-enabled/'+new_instance+'-globaleaks')

    # XXX
    # Create the config file that looks something like this:
    # instance_dir = {{instance_dir}}
    # instances = {{old_instances}},{{new_instance}}:{{port_number}}

