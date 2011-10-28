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
                tmp_j.append(target_id)
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
    def create_target(self, name, category, desc, contact_mail, could_del, initial_hashpass, req_status):
        """
        Creates a new target with the specified parameters.
        Returns the id of the new record.

        |contact_type| supported values: [email]
        |type| supported values: [plain*|pgp]
        |status|: [subscribed*|unsubscribed|selfproposed]
        |could_del|: true or false*, mean: could delete material

        * = default
        """

        if req_status is not "subscribed" and req_status is not "selfproposed":
            print "bad usage of create_target: req_status is different from expected (%s)", req_status
            return 0

        target_id = self._db.target.insert(name=name,
            # groups=pickle.dumps([category]) if category else "",
            desc=desc, contact_type="email",
            contact=contact_mail, type="plain", info="",
            status=req_status, delete_cap=could_del, tulip_counter=0,
            download_counter=0, hashpass=initial_hashpass)
        self._db.commit()
        return target_id

    def delete_target(self, target_id):
        """
        Deletes a target.
        """
        self._db(self._db.target.id==target_id).delete()
        return True

    def get_targets(self, group_set, target_set=[]):
        """
        If target_set is not a list it returns a rowset with all
        targets.
        If target_set is a list of groups it returns a rowset of targets
        that belong to these groups.
        """
        result_id = []
        if not isinstance(group_set, list):
            for target in self._db(self._db.target).select():
                result_id.append(target.id)
        else:
            rows = self._db(self._db.targetgroup).select()
            for row in rows:
                if row.id in group_set:
                    targets = json.loads(row.targets)
                    for t_id in targets:
                        result_id.append(self._db(self._db.target.id==t_id
                                                 ).select().first().id)
        result_id += target_set

        result = []
        for target_id in set(result_id):
            result.append(self.get_target(target_id))

        return result

    def get_target(self, target_id):
        """
        Returns the target with the specified id
        """
        return self._db(self._db.target.id==target_id).select().first()

    def create_tulip(self, leak_id, target_id, hardcoded_url=None):
        """
        Creates a tulip for the target, and inserts it into the db
        (when target is 0, is the whitleblower and hardcoded_url is set by the caller)
        """
        if hardcoded_url and target_id:
            logger.error("Invalid usage of create_tulip: url and target specifyed")
            return NoneType
            
        tulip = self._db.tulip.insert(
            url= hardcoded_url if hardcoded_url else randomizer.generate_tulip_url(),
            leak_id=leak_id,
            target_id=target_id, #FIXME get target_id_properly
            allowed_accesses=0, # inf
            accesses_counter=0,
            allowed_downloads=5,
            downloads_counter=0,
            expiry_time=0)
        self._db.commit()
        return tulip

    def get_leaks(self):
        pass

    def get_leak(self, leak_id):
        pass

    def get_tulips(self, leak_id):
        pass

    def get_tulip(self, tulip_id):
        pass
