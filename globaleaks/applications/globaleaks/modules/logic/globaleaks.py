import randomizer
import time
import pickle


class Globaleaks(object):
    """
    Class that contains useful CRUD methods
    """

    def __init__(self, db):
        self._db = db

    def create_targetgroup(self, name, desc, tags):
        """
        Creates a new targetgroup.
        Returns the id of the new record.
        """
        group_id = self._db.targetgroup.insert(name=name, desc=desc,
                                              tags=tags)
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
            for row in self._db().select(self._db.target.ALL):
                if row.groups:
                    groups_list = pickle.loads(row.groups)
                    groups_list.remove(group_id)
                    self._db(self._db.target.id==row.id).update(
                             groups=pickle.dumps(groups_list))
        self._db.commit()
        return result

    def add_to_targetgroup(self, target_id, group_id):
        """
        Adds the target with id target_id to the targetgroup with id
        group_id.
        Returns True if the operation was successful
        """
        target_row = self._db(self._db.target.id==target_id).select().first()
        group_row = self._db(self._db.targetgroup.id==group_id
                            ).select().first()
        result = False
        if target_row is not None and group_row is not None:
            result = True
            groups_p = target_row.groups
            if not groups_p:
                groups_p = pickle.dumps(set([group_id]))
            else:
                tmp = pickle.loads(groups_p)
                tmp.add(group_id)
                groups_p = pickle.dumps(tmp)
            self._db(self._db.target.id==target_id).update(groups=groups_p)
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
            groups_p = target_row.groups
            if not groups_p:
                groups_p = pickle.dumps(set([group_id]))
            else:
                tmp = pickle.loads(groups_p)
                tmp.remove(group_id)
                groups_p = pickle.dumps(tmp)
            self._db(self._db.target.id==target_id).update(groups=groups_p)
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

        for row in self._db().select(self._db.target.ALL):
            target_data = dict(row)
            if not row.groups:
                continue
            groups = pickle.loads(row.groups)
            for group in groups:
                group_q = self._db(self._db.targetgroup.id==int(group)
                                  ).select().first()
                if not group_q:
                    continue
                result[group_q.id] = {}
                result[group_q.id]["data"] = dict(group_q)
                try:
                    result[group_q.id]["members"].append(target_data)
                except KeyError:
                    result[group_q.id]["members"] = [target_data]
        return result

    def create_target(self, name, category, desc, url, type, info):
        """
        Creates a new target with the specified parameters.
        Returns the id of the new record.
        """
        target_id = self._db.target.insert(name=name,
            groups=pickle.dumps([category]) if category else "",
            desc=desc, url=url, type=type, info=info,
            status="subscribed", tulip_counter=0,
            download_counter=0) #, last_send_tulip=None,
            #last_access=None, last_download=None,
            #tulip_counter=None, download_counter=None
        self._db.commit()
        return target_id

    def delete_target(self, id):
        """
        Deletes a target.
        """
        self._db(self._db.target.id==id).delete()
        return True

    def get_targets(self, target_set):
        """
        If target_set is not a list it returns a rowset with all
        targets.
        If target_set is a list of groups it returns a rowset of targets
        that belong to these groups.
        """
        if not isinstance(target_set, list):
            return self._db(self._db.target).select()
        rows = self._db().select(self._db.target)
        result = []
        for row in rows:
            if row.groups:
                groups = pickle.loads(row.groups)
                done = False
                for elem in target_set:
                    if elem in groups:
                        done = True
                        break
                if done:
                    result.append(row)
        return result

    def get_target(self, target_id):
        """
        Returns the target with the specified id
        """
        return self._db(self._db.target.id==target_id).select().first()

    def create_leak(self, title, desc, leaker, material,
                    target_set, tags="", number=None):
        #FIXME insert new tags into DB first

        #Create leak and insert into DB
        leak_id = self._db.leak.insert(title=title, desc=desc,
                                       submission_timestamp=time.time(),
                                       leaker_id=0, spooled=False)
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
