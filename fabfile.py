import sys
import random
import string
import itertools
import collections
from fabric.api import run, env, put, get, local
try:
    import pystache
except:
    print "Pystache not installed. I will not create apache configs!"

env.use_ssh_config = True

instance_dir = "/data/globaleaks-instances"
instances_config = "/etc/glinstances.conf"
tor_user = 'debian-tor'
hs_base_dir = '/usr/local/var/lib/tor/'
def consume(iterator, n):
    collections.deque(itertools.islice(iterator, n))

class FakeSecHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[asection]\n'
    def readline(self):
        if self.sechead:
            try: return self.sechead
            finally: self.sechead = None
        else: return self.fp.readline()

def _make_tor2web_template():
    tor2web_template = 'tor2web/apache2/tor2web.template'
    f = open(tor2web_template)
    template = ''.join(f.readlines())
    f.close()
    return template

def delete(name):
    run('rm -rf %s/%s' % (instance_dir, name))
    run('rm -rf /data/globaleaks-instances/%s-globaleaks' % name)
    run('rm -rf %shs_%s' % (hs_base_dir, name))
    random_filename = '/tmp/'
    random_filename += ''.join(random.choice(string.ascii_lowercase)
                                for x in range(30))
    get('/etc/glinstances.conf',
            random_filename)
    instance_string = None
    with open(random_filename, 'r') as f:
        import ConfigParser
        config = ConfigParser.SafeConfigParser()
        config.readfp(FakeSecHead(f))
        r_instances = None
        for item, value in config.items('asection'):
            if item == 'instances':
                r_instances = value

    print "[+] Pushing new config file..."
    with open(random_filename, 'w+') as f:
        f.write('# THIS WAS SELF GENERATED\n')
        f.write('instance_dir='+instance_dir+'\n')
        if not r_instances:
            f.write('instances=\n')
        else:
            instances = r_instances.split(',')
            for i in instances:
                if i.startswith(name):
                    continue
                elif not instance_string:
                    instance_string = i
                else:
                    instance_string += ','+i
            instance_string = '' if not instance_string else instance_string
            f.write('instances='+instance_string+'\n')
    put(random_filename, instances_config)

    get('/etc/tor/torrc', random_filename+'.tor')
    lines = []
    with open(random_filename+'.tor', 'r') as f:
        for line in f:
            if name in line:
                lines.pop()
                consume(f, 3)
                continue
            else:
                lines.append(line)


    with open(random_filename+'.new_tor', 'w') as nt:
        for line in lines:
            nt.write(line)
    put(random_filename+'.new_tor', '/etc/tor/torrc')
    local('rm -rf '+random_filename+'*')

def list_instances():
    print "[+] Listing existing instances..."
    output = run('ls '+instance_dir)
    files = output.split()
    instances = []
    print "Currently installed instances"
    print "-----------------------------"
    for f in files:
        if f.startswith('demo'):
            instances.append(f)

        if not f.startswith('template'):
            print "    * %s" % f

    instances.sort()
    print "-----------------------------"
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
                  #'ssl_engine': 'Off',
                  #'path_to_sslcertificate': '',
                  #'path_to_certificate_key': '',
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
    get(instances_config, random_filename+'.cfg')
    with open(random_filename+'.cfg', 'r') as f:
        import ConfigParser
        config = ConfigParser.SafeConfigParser()
        config.readfp(FakeSecHead(f))
        r_instances = None
        for item, value in config.items('asection'):
            if item == 'instances':
                r_instances = value

    print "[+] Pushing new config file..."
    with open(random_filename+'.cfg', 'w+') as f:
        f.write('# THIS WAS SELF GENERATED\n')
        f.write('instance_dir='+instance_dir+'\n')
        if not r_instances:
            f.write('instances='+new_instance+':'+port_number+'\n')
        else:
            f.write('instances='+r_instances+','+new_instance+':'+port_number+'\n')

    put(random_filename+'.cfg', instances_config)

    # XXX Update torrc and restart the globaleaks init script. Get hidden
    # service of latest instance.
    print "[+] Getting remote torrc file..."
    get('/etc/tor/torrc', random_filename+'.tor')

    HSDir = hs_base_dir + 'hs_' + new_instance + '/'
    with open(random_filename+'.tor', 'a+') as f:
        f.write('\n\n# This part of config was auto generated\n')
        f.write('HiddenServiceDir %s\n' % HSDir)
        f.write('HiddenServicePort 80 127.0.0.1:%s\n' % port_number)
        f.write('# end\n')

    run('mkdir -p %s' % HSDir)
    run('chown -R %s %s' % (tor_user, HSDir))

    print "[+] Pushing new torrc config file..."
    put(random_filename+'.tor', '/etc/tor/torrc')
    run('/etc/init.d/tor restart')
    dot_onion = run('cat %s/hostname' % HSDir)

    print "[+] Replacing known values in globaleaks template"
    with open(random_filename+'.gl', 'w+') as gf:
        with open('globaleaks/defaults/original.globaleaks.conf') as f:
            for line in f:
                if line.strip().startswith('hsurl'):
                    print l
                    l = line.replace('oooooooooooooooo.onion', dot_onion)
                elif line.strip().startswith('baseurl'):
                    print l
                    l = line.replace('https://example.com', 'http://'+server_name)
                elif line.strip().startswith('server_port'):
                    print l
                    l = line.replace('8000', port_number)
                elif line.strip().startswith('server_ip'):
                    l = line.replace('127.0.0.1', env.host)
                    print l
                else:
                    l = line
                gf.write(l)

    print "[+] Pushing globaleaks.conf file to remote host"
    put(random_filename+'.gl',
            instance_dir+'/'+new_instance+'/globaleaks/globaleaks.conf')

    print "[+] Setting proper permissions..."
    run('chown -R globaleaks:globaleaks '+instance_dir+'/'+new_instance)

    print "[+] Cleaning up tmp files"
    local('rm -rf %s*' % random_filename)

    print "[+] Restarting Globaleaks-service"
    run('/etc/init.d/globaleaks-service restart')
    run('/etc/init.d/apache2 reload')

    print "[+] Created new globaleaks instance!"
    print ""
    print "Details"
    print "-------"
    print "Hostname: "+server_name
    print "Local Port: "+port_number
    print "Hidden Service: "+dot_onion

