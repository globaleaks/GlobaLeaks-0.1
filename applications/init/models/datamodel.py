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
        #FIXME: raise error that id can not be changed
        pass
    id = property(get_id, set_id)
    
    def get_title(self):
        return db.leak[self.id].title
    def set_title(self, title):
        db.leak[self.id] = dict(title = title)
        db.commit()
    title = property(get_title, set_title)
    
    #TODO: implment get/set tags
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
    
    #TODO: implment get/set material
    def get_material(self):
        pass
    def set_material(self, material):
        pass
    material = property(get_material, set_material)
    
    #TODO: implment get/set targets
    def get_targets(self):
        pass
    def set_targets(self, targets):
        pass
    targets = property(get_targets, set_targets)
    
    def get_submission_timestamp(self):
        return db.leak[self.id].submission_timestamp
    def set_submission_timstamp(self, timestamp):
        #FIXME: raise error that submission timestamp can not be changed
        pass
    submission_timestamp = property(get_submission_timestamp, set_submission_timstamp)
    
    def get_leaker(self):
        pass
    def set_leaker(self, leaker):
        #FIXME: raise error that leaker can not be changed
        pass
    leaker = property(get_leaker, set_leaker)
    
    def get_tulips(self):
        for tulip_id in db(db.tulip.leak_id==self._id).select(db.tulip.id):
            yield Tulip(tulip_id["id"])
        
    def set_tulips(self, tulips):
        #FIXME: raise error that tulip can not be changed
        pass
    tulips = property(get_tulips, set_tulips)


class Tulip(object):
    def __init__(self, id=None, url=None):
        if url:
            self._id = db(db.tulip.uri==url).select().first().id
        else:
            self._id = id
        
    def get_id(self):
        return self._id
    def set_id(self, id):
        #FIXME: raise error that id of a tulip can not be changed
        pass
    id = property(get_id, set_id)
    
    def get_url(self):
        return db.tulip[self.id].uri
    def set_url(self, url):
        #FIXME: raise error that id of a tulip can not be changed
        pass
    url = property(get_url, set_url)
    
    def get_target(self):
        return db.tulip[self.id].target_id
    def set_target(self, target):
        #FIXME: raise error that id of a tulip can not be changed
        pass
    target = property(get_target, set_target)
   
    def get_allowed_downloads(self):
        return db.tulip[self.id].url
    def set_allowed_downloads(self, allowed_downloads):
        #FIXME: raise error that id of a tulip can not be changed
        pass
    allowed_downloads = property(get_allowed_downloads, set_allowed_downloads)
    
    def get_leak(self):
        return Leak(db.tulip[self.id].leak_id)
    def set_leak(self):
        #FIXME: raise error that leak of a tulip can not be changed
        pass
    leak = property(get_leak, set_leak)
