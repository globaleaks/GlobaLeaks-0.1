import time
from datamodel import Leak
from randomizer import randomizer
from sql import db

class Globaleaks(object):

    def __init__(self):
        pass
        
    def create_target(self):
        pass
        
    def get_targets(self):
        pass
        
    def get_target(self, target_id):
        pass
        
    def create_leak(self, title, desc, leaker, material, targets = {}, tags =[]):
        #FIXME insert new tags into DB first
        
        #Create leak and insert into DB
        leak_id = db.leak.insert(title = title, desc = desc,
            submission_timestamp = time.time(),
            leaker_id = 0)
        
        #Create a tulip for each target and insert into DB
        for target_uri, allowed_downloads in targets.iteritems():
            db.tulip.insert(uri = randomizer.generate_tulip_url(),
                leak_id = leak_id,
                target_id = target_uri, #FIXME get target_id_properly
                downloads_counter = 0,
                allowed_downloads = allowed_downloads,
                expiry_time = 0)
        
        db.commit()
        return leak_id
        
    def get_leaks(self):
        pass
        
    def get_leak(self, leak_id):
        pass
        
    def get_tulips(self, leak_id):
        pass
        
    def get_tulip(self, tulip_id):
        pass


gl = Globaleaks()

id = gl.create_leak("First Leak", "A sample leak on how DDB is working with the FBI",
        None, None, {"Al Jazeera":10 , "CNN":20})

leak = Leak(id)
for tulip in leak.tulips:
    print tulip.url


