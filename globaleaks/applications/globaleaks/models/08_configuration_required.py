def configuration_required(funct):
    """
    This function is called ahead of every controller function that
    require to run in a proper configured GlobaLeaks environment.
    """

    admin_row = db(db.auth_user.username == 'admin').select().first()
    if not admin_row:
        return lambda: redirect('/globaleaks/installation/mandatory_setup.html')
    else:
        return funct
