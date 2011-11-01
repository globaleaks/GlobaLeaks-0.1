import pickle
from gluon.contrib import simplejson as json

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

    def get_files(self):
        files = db.material[self.id].file
        return pickle.loads(files)

    def set_files(self, id):
        print "Error: url is read only"
        pass

    files = property(get_files, set_files)

    @staticmethod
    def create_new(leak_id, url, type, file):
        return db.material.insert(leak_id=leak_id,
            url=None, type=None, file=file)

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

    def get_whistleblower_access(self):
        return db.leak[self.id].whistleblower_access

    def set_whistleblower_access(self, whistleblower_access):
        db.leak[self.id].whistleblower_access
        db.commit()

    whistleblower_access = property(get_whistleblower_access, set_whistleblower_access)

    #TODO: implement get/set material
    def get_material(self):
        return db(db.material.leak_id==self._id).select(db.material.ALL).first()

    def set_material(self, material):
        pass

    material = property(get_material, set_material)

    def get_spooled(self):
        return db.leak[self.id].spooled

    def set_spooled(self, material):
        pass

    spooled = property(get_spooled, set_spooled)

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

    def add_material(self, leak_id, url, type, file):
        Material.create_new(leak_id, url, type, file)

    def get_extra(self):
        extra = {}
        for row in db(db.leak.id==self._id).select():
            for i in settings.extrafields.fields:
                extra[i['name']] = row[i['name']]
        return extra

    def get_notified_targetgroups(self):
        """
        Returns a list of ids of the groups that had been notified of
        this leak
        """
        notified = db.leak[self.id].notified_groups
        if notified is None:
            return []
        else:
            return json.loads(notified)

    def notify_targetgroup(self, group_id):
        """
        Notifies the targets of the selected targetgroup that have not
        been notified yet. Then adds that group to the notified_groups
        list
        """
        
        notified_groups = self.get_notified_targetgroups()
        notified_targets = [x.id for x in gl.get_targets(notified_groups)]
        to_notify = [x.id for x in gl.get_targets([group_id])]
        to_notify = set(to_notify).difference(notified_targets)
        for target_id in to_notify:
            target = gl.get_target(target_id)
            previously_generated = [tulip.target for tulip in self.tulips]
            # generate a tulip for targets thats haven't one
            if target not in previously_generated:
                tulip_id = gl.create_tulip(self._id, target.id)
            tulip_url = db.tulip[tulip_id].url
            if target.status == "subscribed":
                # Add mail to db, sending managed by scheduler
                db.mail.insert(target=target.name,
                               address=target.contact,
                               tulip=tulip_url)
        notified_groups += [group_id]
        notified_groups = list(set(notified_groups))  # deletes duplicates
        
        db.leak[self._id].update_record(
            notified_groups=json.dumps(notified_groups))
        db.commit()

class Target(object):
    def __init__(self, id):
        self._id = id

    def get_id(self):
        return self._id

    def set_id(self):
        print "Error: id is read only"
        pass

    id = property(get_id, set_id)

class TargetList(object):
    def __init__(self, g=None):
        if g:
            self.build(g)

    def build(self, g):
        """for t in tlist:
            db.target.insert(name=t[0].name, desc=t[0].desc,
                            url=t[0].url, type=t[0].type,
                            info=t.info, status="active",
                            group=t.Name)
        """
        db.targetgroup.insert(name=g.Name, desc=g.Description, tags=g.Tags)
            

    def get_list(self):
        for group in db().select(db.targetgroup.ALL):
            yield group
        pass
    def set_list(self, value):
        pass
    list = property(get_list, set_list)

    def get_name(self):
        pass
    def set_name(self, value):
        pass
    name = property(get_name, set_name)

    def get_desc(self):
        pass
    def set_desc(self, value):
        pass
    desc = property(get_desc, set_desc)

    def get_url(self):
        pass
    def set_url(self, value):
        pass
    url = property(get_url, set_url)

    def get_type(self):
        pass
    def set_type(self, value):
        pass
    type = property(get_type, set_type)

    def get_info(self):
        pass
    def set_info(self, value):
        pass
    info = property(get_info, set_info)

class Tulip(object):
    def __init__(self, id=None, url=None):
        if url:
            self._id = db(db.tulip.url==url).select().first().id
        else:
            self._id = id

    def get_vote(self):
        return db.tulip[self.id].express_vote

    def set_vote(self, vote):
        # acceptable range is -1 0 and +1
        if(vote >= (-1) and vote <= 1):
            db.tulip[self.id].update_record(express_vote=vote)
            db.commit()
        else:
            print "Error: tulip vote has range of -1, 0 and +1"

    vote = property(get_vote, set_vote)

    # LOL! Vecnish hit's again..
    # XXX rename this function to "get_pertinence"
    def get_pertinentness(self):
        pertinentness = 0
        brotherTulips = db(db.tulip.leak_id == db.tulip[self.id].leak_id).select()
        for t in brotherTulips:
            if t.express_vote and t.target_id:
                pertinentness += int(t.express_vote)
        return pertinentness

    def set_pertinentness(self, value):
        print "Error: pertinentness is a collaborative value"

    pertinentness = property(set_pertinentness, get_pertinentness)

    # delete_bros used to delete the tulip self and all the legit brothers
    def delete_bros(self):
        retval = db(db.tulip.leak_id == db.tulip[self.id].leak_id).count()
        db(db.tulip.leak_id == db.tulip[self.id].leak_id).delete()
        return retval

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

    def get_feedbacks_provided(self):
        return db.tulip[self.id].feedbacks_provided

    def set_feedbacks_provided(self, feed_numbers):
        db.tulip[self.id].update_record(feedbacks_provided=feed_numbers)
        db.commit()

    feedbacks_provided = property(get_feedbacks_provided, set_feedbacks_provided)

    def get_leak(self):
        return Leak(db.tulip[self.id].leak_id)

    def set_leak(self):
        print "Error: leak is read only"
        pass

    leak = property(get_leak, set_leak)
