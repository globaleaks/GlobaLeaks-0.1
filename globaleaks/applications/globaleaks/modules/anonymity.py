from __future__ import with_statement

import re
import os.path
import signal
import subprocess
import socket
import threading
import time
import logging

from pytorctl import TorCtl

from config import projroot

torrc = os.path.join(projroot, 'globaleaks', 'tor', 'torrc')
hiddenservice = os.path.join(projroot, 'globaleaks', 'tor', 'hiddenservice')

class ThreadProc(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.proc = None

    def run(self):
        try:
            self.proc = subprocess.Popen(self.cmd,
                                         shell = False, stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE)
        except OSError:
           logging.fatal('cannot execute command')

class Tor:
    def __init__(self, s):
        self.settings = s
        if self.settings.globals.torifyconnections or self.settings.globals.hiddenservice:
            self.start()

    def check(self):
        conn = TorCtl.connect()
        if conn != None:
            conn.close()
            return True

        return False

    def get_hiddenservicename(self):
        name = ""
        if self.settings.globals.hiddenservice and self.check():
            hostnamefile = os.path.join(hiddenservice, 'hostname')
            while True:
                if not os.path.exists(hostnamefile):
                    time.sleep(1)
                    continue

                with open(hostnamefile, 'r') as f:
                    name = f.readline().strip()
                    break
        return name
            

    def start(self):
        if not self.check():

            if not os.path.exists(torrc):
                raise OSError("torrc doesn't exist (%s)" % torrc)

            tor_cmd = ["tor", "-f", torrc]
 
            if self.settings.globals.hiddenservice:
                tor_cmd.extend(["--HiddenServiceDir", hiddenservice, "--HiddenServicePort", "80 127.0.0.1:8000"])

            torproc = ThreadProc(tor_cmd)
            torproc.run()

            bootstrap_line = re.compile("Bootstrapped 100%: ")

            while True:
                if torproc.proc == None:
                    time.sleep(1)
                    continue

                init_line = torproc.proc.stdout.readline().strip()
                if not init_line:
                    torproc.proc.kill()
                    return False

                if bootstrap_line.search(init_line):
                    break

            return True

    def stop(self):
        if not self.check():
            return

        conn = TorCtl.connect()
        if conn != None:
            conn.send_signal("SHUTDOWN")
            conn.close()

class TorAccessCheck:
    def __init__(self, ip, headers):
            self.result = {}
            self.check(ip, headers)

    def check_tor2web(self, headers):
        """
        This is used to parse tor2web headers.
        The header format should be
        X-tor2web: encrypted|plain-trusted|untrusted-tor|notor
        """
        encryption = None
        trust = None
        withtor = None

        try:
            parsed = headers.http_x_tor2web.split('-')
        except:
            return False
        try:
            if parsed[0] == "plain":
                try:
                    if parsed[1] == "tor":
                        tor = True
                    else:
                        tor = False
                except:
                    tor = False

                encryption = False
                trust = False

            elif parsed[0] == "encrypted":
                encryption=True
                if parsed[1] == "trusted":
                    trust = True
                elif parsed[1] == "untrusted":
                    trust = False
                else:
                    trust = None

                if parsed[2] == "tor":
                    withtor = True
                elif parsed[2] == "notor":
                    withtor = False
        except:
            # XXX add error handling here.
            pass

        return dict(encryption=encryption, \
                    trust=trust, tor=withtor)


    def check_tor(self, ip):
        if str(ip) == "127.0.0.1":
            return True
        else:
            return False

    def check(self, ip, headers):
        self.result['tor2web'] = self.check_tor2web(headers)

        if not self.result['tor2web']:
            self.result['tor'] = self.check_tor(ip)
        else:
            self.result['tor'] = self.result['tor2web']['tor']

