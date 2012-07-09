#coding: utf-8
"""
This controller module contains every controller that the target can use
to edits its settings. (E.g.: Unsubscribe from a GL node)
"""

@configuration_required
def index():
    return dict(message="hello from target.py")

def valid_pgp_key(pgpkeystring):
    # implementation TODO: 
    # verify that is a valid PGP string, almost checking the header 
    return True

@configuration_required
def bouquet():
    """
    This page is indexed by an uniq identifier by the receiver, and shows
    all accessible Tulips, its the page where she/he could change their
    preferences
    """
    if request and request.args:
        target_url = request.args[0]
    else:
        return dict(err="Tulip index not supplied")

    tulip = Tulip(url=target_url)
    if tulip.id == -1:
        return dict(err="Invalid Tulip")

    receiver_row = db(db.target.id==tulip.target_id).select()

    print receiver_row[0]

    # pretty string for password default
    if receiver_row[0]['password'] != None:
        passlen = str(len(receiver_row[0]['password']))
        password_default = "Password set and enabled (" + passlen + " char)"
    else:
        password_default= "password not configured"

    security_input = (
        Field('password', requires=IS_LENGTH(minsize=8), default=password_default),
        Field('confirm_password', 
            requires=IS_EQUAL_TO(request.vars.password, error_message="passwords do not match")),
        Field('pgpkey', 'text', default=receiver_row[0]['pgpkey'] ),
        Field('pgpkey_enabled', 'boolean', default=False),
    )

    security_form = SQLFORM.factory(*security_input, table_name="security")

    if security_form.accepts(request.vars, session, keepvalues=True):

        pref = request.vars

        if len(pref.password) > 7:
            # TODO: hash them before store
            db.target[receiver_row[0].id].update_record(password=pref.password)
            # Issue: https://github.com/globaleaks/GlobaLeaks/issues/13
            # specifiy some feature that can't be implemented now (mail notification)
            db.target[receiver_row[0].id].update_record(password_enabled=True)
            db.commit()
            print "saved password " + pref.password

        if len(pref.pgpkey) > 20:

            if not valid_pgp_key(pref.pgpkey):
                return dict(err="Invalid PGP key submitted")

            db.target[receiver_row[0].id].update_record(pgpkey=pref.pgpkey)
            db.commit()
            print "Key saved for target " + str(receiver_row[0].id)

        if pref.pgpkey_enabled == True:
            db.target[receiver_row[0].id].update_record(pgpkey_enabled=True)
            db.commit()
            print "Key set as enable, for target " + str(receiver_row[0].id)

    # this require to be splitted because tulip are leak x target matrix
    bouquet_list = []
    tulip_list = db(db.tulip.target_id==receiver_row[0].id).select()
    for single_t in tulip_list:
        bouquet_list.append(single_t)

    return dict(err=False,
                bouquet=bouquet_list,
                target=receiver_row[0],
                security=security_form)

