import randomizer
import time
from gluon.contrib import simplejson as json

class Globaleaks(object):
    """
    Class that contains useful CRUD methods
    """

    def __init__(self, db):
        self._db = db

    def create_targetgroup(self, name, desc, tags, targets=None):
        """
        Creates a new targetgroup.
        Returns the id of the new record.
        """
        group_id = self._db.targetgroup.insert(name=name, desc=desc,
                                              tags=tags, targets=targets)
        self._db.commit()
        return group_id

    def delete_targetgroup(self, group_id):
        """
        Deletes the targetgroup with the specified id.
        Returns True if the operation was successful.
        """
        result = False
        if self._db(self._db.targetgroup.id==group_id).select():
            result = True
            self._db(self._db.targetgroup.id==group_id).delete()
        self._db.commit()
        return result

    def update_targetgroup(self, group_id, **kwargs):
        """
        Changes the name field of the targetgroup with the specified id.
        """
        result = False
        if self._db(self._db.targetgroup.id==group_id).select():
            result = True
            self._db(self._db.targetgroup.id==group_id).update(**kwargs)
            self._db.commit()
        return result

    def get_group_id(self, group_name):
        return self._db(self._db.targetgroup.name==group_name
                       ).select().first().id

    def add_to_targetgroup(self, target_id, group_id=None, group_name=None):
        """
        Adds the target with id target_id to the targetgroup with id
        group_id.
        Returns True if the operation was successful
        """
        if group_name:
            group_id = self.get_group_id(group_name)
        target_row = self._db(self._db.target.id==target_id).select().first()
        group_row = self._db(self._db.targetgroup.id==group_id
                            ).select().first()
        result = False
        if target_row is not None and group_row is not None:
            targets_j = group_row.targets
            if not targets_j:
                # Dumps the json to the group table
                targets_j = json.dumps([target_id])
            else:
                tmp_j = json.loads(targets_j)
                tmp_j.append(group_id)
                targets_j = json.dumps(tmp_j)
            result = self._db(self._db.targetgroup.id==group_id
                             ).update(targets=targets_j)
            self._db.commit()

        return result

    def remove_from_targetgroup(self, target_id, group_id):
        """
        Removes a target from a group.
        Returns True if the operation was successful.
        """
        target_row = self._db(self._db.target.id==target_id).select().first()
        group_row = self._db(self._db.targetgroup.id==group_id
                            ).select().first()
        result = False
        if target_row is not None and group_row is not None:
            result = True
            targets_j = group_row.targets

            if not targets_j:
                targets_j = json.dumps([target_id])
            else:
                tmp = json.loads(targets_j)
                tmp.remove(target_id)
                targets_j = json.dumps(tmp)

            self._db(self._db.targetgroup.id==group_id
                    ).update(targets=targets_j)
            self._db.commit()
        return result

    def get_targetgroups(self):
        """
        Returns a dictionary that has the targetgroup ids as keys and
        another dictionary as value.
        This second dictionary has field "data" with group data and
        field "members" which is a list of targets that belong to that
        group.
        """
        result = {}
        for row in self._db().select(self._db.targetgroup.ALL):
            result[row.id] = {}
            result[row.id]["data"] = dict(row)
            result[row.id]["members"] = []

            if result[row.id]["data"]['targets']:
                members = result[row.id]["data"]['targets']
                for member in json.loads(members):
                    member_data  =self._db(self._db.target.id==int(member)
                                          ).select().first()
                    result[row.id]["members"].append(dict(member_data))
            else:
                result[row.id]["members"] = []
        return result

    # by default, a target is inserted with an email type only as contact_type,
    # in the personal page, the receiver should change that or the contact type 
    # (eg: facebook, irc ?, encrypted mail setting up a gpg pubkey)
    def create_target(self, name, category, desc, contact_mail, initial_hashpass, req_status):
        """
        Creates a new target with the specified parameters.
        Returns the id of the new record.

        |contact_type| supported values: [email]
        |type| supported values: [plain*|pgp]
        |status|: [subscribed*|unsubscribed|selfproposed]

        * = default
        """

        if req_status is not "subscribed" and req_status is not "selfproposed":
            print "bad usage of create_target: req_status is different from expected (%s)", req_status
            return 0

        target_id = self._db.target.insert(name=name,
            # groups=pickle.dumps([category]) if category else "",
            desc=desc, contact_type="email", 
            contact=contact_mail, type="plain", info="",
            status=req_status, tulip_counter=0,
            download_counter=0, hashpass=initial_hashpass) 
        self._db.commit()
        return target_id

    def delete_target(self, target_id):
        """
        Deletes a target.
        """
        self._db(self._db.target.id==target_id).delete()
        return True

    # uniq() by http://www.peterbe.com/plog/uniqifiers-benchmark
    def f7(self, seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if x not in seen and not seen_add(x)]

    def get_targets(self, target_set):
        """
        If target_set is not a list it returns a rowset with all
        targets.
        If target_set is a list of groups it returns a rowset of targets
        that belong to these groups.
        """
        if not isinstance(target_set, list):
            return self._db(self._db.target).select()
         
        target_rows = self._db(self._db.target).select()
        group_rows = self._db(self._db.targetgroup).select()

        target_id_list = []
        for g in group_rows:
            if str(g.id) in target_set:
                # XXX maybe it is not very clean...
                for single_target_id in g.targets.replace('"', "'"):
                    try:
                        intval = int(single_target_id, 10)
                        target_id_list.append(intval)
                    except ValueError:
                        pass
       
        results = []             
        if not len(target_id_list):
            return results
               
        target_id_list = self.f7(target_id_list)
                           
        for t in target_rows:
            for choosen in target_id_list:
                if choosen == t.id:
                    results.append(t)     
 
        return results

    def get_target(self, target_id):
        """
        Returns the target with the specified id
        """
        return self._db(self._db.target.id==target_id).select().first()

    def create_leak(self, id_, target_set, number=None):
                    #title, desc, leaker, material,
                    #target_set, tags="", number=None):
        #FIXME insert new tags into DB first
        #Create leak and insert into DB
        leak_id = id_ #self._db.leak.insert(title=title, desc=desc,
                  #                     submission_timestamp=time.time(),
                  #                     leaker_id=0, spooled=False)
        targets = self.get_targets(target_set)

        for t in targets:
        #Create a tulip for each target and insert into DB
        #for target_url, allowed_downloads in targets.iteritems():
            self._db.tulip.insert(
                url=randomizer.generate_tulip_url(),
                leak_id=leak_id,
                target_id=t.id, #FIXME get target_id_properly
                allowed_accesses=0, # inf
                accesses_counter=0,
                allowed_downloads=5,
                downloads_counter=0,
                expiry_time=0)
        
        # tulip for the whistleblower
        self._db.tulip.insert(
                url=number,
                leak_id=leak_id,
                target_id=0, #FIXME get target_id_properly
                allowed_accesses=0, # inf
                accesses_counter=0,
                allowed_downloads=5,
                downloads_counter=0,
                expiry_time=0)

        self._db.commit()
        return leak_id

    def get_leaks(self):
        pass

    def get_leak(self, leak_id):
        pass

    def get_tulips(self, leak_id):
        pass

    def get_tulip(self, tulip_id):
        pass
