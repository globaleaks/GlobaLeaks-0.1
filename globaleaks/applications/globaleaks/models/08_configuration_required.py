def configuration_required(funct):
    """
    This function is called ahead of every controller function that
    require to run in a proper configured GlobaLeaks environment.
    Is checked the presence of the node_admin_configured, set as true
    when the mandatory configuartion is provieded
    """

    admin_row = db(db.auth_user.username == 'admin').select().first()
    if not admin_row:
        return lambda: redirect('/globaleaks/installation/mandatory_setup.html')
    else:
        return funct
