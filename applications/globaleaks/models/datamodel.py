import time

# web2py's funny way to import "local" modules
#db = local_import('sql').db
#randomizer = local_import('randomizer')

randomizer = local_import('randomizer')

class Leak(object):
    def __init__(self, id):
        self._id = id
    
    def get_id(self):
        return self._id
    def set_id(self):
        print "Error: id is read only"
        pass
    id = property(get_id, set_id)
    
    def get_title(self):
        return db.leak[self.id].title
    def set_title(self, title):
        db.leak[self.id] = dict(title = title)
        db.commit()
    title = property(get_title, set_title)
    
    #TODO:implement get/set tags
    def set_tags(self):
        pass
    def get_tags(self):
        pass
    tags = property(get_tags, set_tags)

    def get_desc(self):
        return db.leak[self.id].desc
    def set_desc(self, desc):
        db.leak[self.id].desc = desc
        db.commit()
    desc = property(get_desc, set_desc)
    
    #TODO: implement get/set material
    def get_material(self):
        for material_id in db(db.material.leak_id==self._id).select(db.material.id):
            yield Material(material_id)
    def set_material(self, material):
        pass
    material = property(get_material, set_material)
    
    #TODO: implement get/set targets
    def get_targets(self):
        pass
    def set_targets(self, targets):
        pass
    targets = property(get_targets, set_targets)
    
    def get_submission_timestamp(self):
        return db.leak[self.id].submission_timestamp
    def set_submission_timstamp(self, timestamp):
        print "Error: submission_timestamp is read only"
        pass
    submission_timestamp = property(get_submission_timestamp, set_submission_timstamp)
    
    def get_leaker(self):
        pass
    def set_leaker(self, leaker):
        print "Error: leaker is read only"
        pass
    leaker = property(get_leaker, set_leaker)
    
    def get_tulips(self):
        for tulip_id in db(db.tulip.leak_id==self._id).select(db.tulip.id):
            yield Tulip(tulip_id["id"])
        
    def set_tulips(self, tulips):
        print "Error: tulip is read only"
        pass
    tulips = property(get_tulips, set_tulips)
    
    def add_material(self, leak_id, url, type):
        Material.create_new(leak_id, url, type)


class Tulip(object):
    def __init__(self, id=None, url=None):
        if url:
            self._id = db(db.tulip.url==url).select().first().id
        else:
            self._id = id
        
    def get_id(self):
        return self._id
    def set_id(self, id):
        print "Error: id is read only"
        pass
    id = property(get_id, set_id)
    
    def get_url(self):
        return db.tulip[self.id].url
    def set_url(self, url):
        print "Error: url is read only"
        pass
    url = property(get_url, set_url)
    
    def get_target(self):
        return db.tulip[self.id].target_id
    def set_target(self, target):
        print "Error: target is read only"
        pass
    target = property(get_target, set_target)

    def get_allowed_accesses(self):
        return db.tulip[self.id].allowed_accesses
    def set_allowed_accesses(self, allowed_accesses):
        db.tulip[self.id].update_record(allowed_accessess=allowed_accesses)
        db.commit()
    allowed_accesses = property(get_allowed_accesses, set_allowed_accesses)

    def get_accesses_counter(self):
        return db.tulip[self.id].accesses_counter
    def set_accesses_counter(self, accesses_counter):
        db.tulip[self.id].update_record(accesses_counter=accesses_counter)
        db.commit()
    accesses_counter = property(get_accesses_counter, set_accesses_counter)
   
    def get_allowed_downloads(self):
        return db.tulip[self.id].allowed_downloads
    def set_allowed_downloads(self, allowed_downloads):
        db.tulip[self.id].update_record(allowed_downloads=allowed_downloads)
        db.commit()
    allowed_downloads = property(get_allowed_downloads, set_allowed_downloads)
    
    def get_downloads_counter(self):
        return db.tulip[self.id].downloads_counter
    def set_downloads_counter(self, downloads_counter):
        db.tulip[self.id].update_record(downloads_counter=downloads_counter)
        db.commit()
    downloads_counter = property(get_downloads_counter, set_downloads_counter)
    
    def get_leak(self):
        return Leak(db.tulip[self.id].leak_id)
    def set_leak(self):
        print "Error: leak is read only"
        pass
    leak = property(get_leak, set_leak)
    
class Material(object):
    def __init__(self, id, url=None):
        if url:
            self._id = db(db.tulip.url==url).select().first().id
        else:
            self._id = id
        
    def get_id(self):
        return self._id
    def set_id(self, id):
        print "Error: id is read only"
        pass
    id = property(get_id, set_id)
    
    def get_url(self):
        return db.material[self.id].url
    def set_url(self, id):
        print "Error: url is read only"
        pass
    url = property(get_url, set_url)
    
    def get_type(self):
        return db.material[self.id].type
    def set_type(self, id):
        print "Error: url is read only"
        pass
    type = property(get_type, set_type)
    
    @staticmethod
    def create_new(leak_id, url, type):
        return db.material.insert(leak_id=leak_id,
            url="demo", type="demo")
