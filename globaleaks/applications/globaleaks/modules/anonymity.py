import socket

class Tor:
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
         
