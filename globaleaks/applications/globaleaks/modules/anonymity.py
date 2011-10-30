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

class TorHiddenServiceProc(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.proc = None

    def run(self):
        try:
            self.proc = subprocess.call(["tor", "-f", torrc,
                                         "--HiddenServiceDir", hiddenservice,
                                         "--HiddenServicePort", "80 127.0.0.1:8000"],
                                         shell = False, stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE)
        except OSError:
           logging.fatal('tor: command not found')

class TorHiddenService:
    def __init__(self, s):
        self.settings = s
        self.name = None
        if self.settings.private.hiddenservice:
            self.start()

    def check(self):
        conn = TorCtl.connect()
        if not conn:
            conn.close()
            return True

        return False

    def start(self):
        if not self.check():

            if not os.path.exists(torrc):
                raise OSError("torrc doesn't exist (%s)" % torrc)

            torproc = TorHiddenServiceProc()
            torproc.run()

            bootstrap_line = re.compile("Bootstrapped 100%: ")

            hiddenservicename = None

            while True:
                if torproc.proc == None:
                    sleep(1)
                    continue

                init_line = torproc.proc.stdout.readline().strip()

                if not init_line:
                    torproc.proc.kill()
                    return False

                if bootstrap_line.search(init_line):
                    break;

            hostnamefile = os.path.join(hiddenservice, 'hostname')
            while True:
                if not os.path.exist(hostnamefile):
                    sleep(1)
                    continue

                with open(hostnamefile, 'r') as f:
                    self.name = f.readline().strip()
                break

            self.settings.private.hiddenservice = True

            return True

    def stop(self):
        if not self.check():
            return

        conn = TorCtl.connect()
        if conn != None:
            conn.send_signal("SHUTDOWN")
            conn.close()

        self.name = None
        self.settings.private.hiddenservice = False

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

