#
# EXPERIMENTAL CODE - TO BE COMPLETED
#
# Notes for supporting PGP encryption
# Requires: python-gnupg
#           pip install python-gnupg

import gnupg


class PGP:
    def __init__(self, directory, keyserver=None):
        if keyserver:
            self.keyserver = keyserver
        else:
            self.keyserver = 'pgp.mit.edu'
        self.gpg = gnupg.GPG(gnupghome=directory)

    def get_key(self, keyid, fp = None):
        r_key = self.gpg.recv_keys(self.keyserver, keyid)
        if fp:
            if r_key.fingerprints[0] == fp:
                print "Fingerprint match"
            else:
                print "ERROR: Fingerprints do not match!"

    def encrypt(self, data, dst):
        return self.gpg.encrypt(data, dst, always_trust=True)


# Example usage
crypt = PGP("/tmp/globaleaks", "pgp.mit.edu")
crypt.get_key("150FE210", "46E5EF37DE264EA68DCF53EAE3A21297150FE210")
print "This is the Encrypted message:"
print crypt.encrypt("Hello :)", "art@fuffa.org")

