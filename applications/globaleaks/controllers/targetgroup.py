import pickle

@auth.requires_login()
def index():
    """
    Extracts targets and their groups from db
    """
    all_targets = []
    result = {}
    for row in db().select(db.target.ALL):
        target_data = dict(row)
        all_targets.append(target_data)
        if not row.groups:
            continue
        groups = pickle.loads(row.groups)
        for group in groups:
            group_q = db(db.targetgroup.id==int(group)).select().first()
            if not group_q:
                continue
            group_data = dict(group_q)
            if not result.has_key(group_q.id):
                result[group_q.id] = {}
            if not result[group_q.id].has_key("data"):
                result[group_q.id]["data"] = dict(group_q)
            try:
                result[group_q.id]["members"].append(target_data)
            except KeyError:
                result[group_q.id]["members"] = [target_data]
    print result
    print all_targets
    return dict(message="hello from targetgroup.py",
                all_targets=all_targets, targetgroups=result)

@auth.requires_login()
def create():
    """
    Receives parameters "name", "desc", and "tags" from POST.
    Creates a new target group with the specified parameters
    """
    # XXX fix to POST! get only for test
    try:
        name = request.get_vars["name"]
        desc = request.get_vars["desc"]
        tags = request.get_vars["tags"]
    except KeyError:
        return response.json({'success':'false'})
    else:
        db.targetgroup.insert(name=name,
                              desc=desc,
                              tags=tags)
        db.commit()
        return response.json({'success':'true'})

@auth.requires_login()
def add():
    """
    Receives parameters "target" and "group" from POST.
    Adds taget to group.
    """
    # XXX fix to POST! get only for test
    try:
        target_id = request.get_vars["target"]
        group_id = request.get_vars["group"]
    except KeyError:
        pass
    else:
        target_row = db(db.target.id==target_id).select().first()
        group_row = db(db.targetgroup.id==group_id).select().first()

        if target_row is not None and group_row is not None:
            groups_p = target_row.groups
            if not groups_p:
                groups_p = pickle.dumps(set([group_id]))
            else:
                tmp = pickle.loads(groups_p)
                tmp.add(group_id)
                groups_p = pickle.dumps(tmp)
            db(db.target.id==target_id).update(groups=groups_p)
            db.commit()
            return response.json({'success':'true'})

    return response.json({'success':'false'})


@auth.requires_login()
def remove():
    """
    Receives parameters "target" and "group" from POST.
    Removes taget from group.
    """
    # XXX fix to POST! get only for test
    try:
        target_id = request.get_vars["target"]
        group_id = request.get_vars["group"]
    except KeyError:
        pass
    else:
        target_row = db(db.target.id==target_id).select().first()
        group_row = db(db.targetgroup.id==group_id).select().first()

        if target_row is not None and group_row is not None:
            groups_p = target_row.groups
            if groups_p:
                tmp = pickle.loads(groups_p)
                try:
                    tmp.remove(group_id)
                except KeyError:
                    pass
                else:
                    groups_p = pickle.dumps(tmp)
                    db(db.target.id==target_id).update(groups=groups_p)
                    db.commit()
            return response.json({'success':'true'})

    return response.json({'success':'false'})
