def configuration_required(funct):
    """
    This function is called ahead of every controller function that
    require to run in a proper configured GlobaLeaks environment.

    administrative access is required two times (the first for setup a simple
    password, the second with the hidden service started. This mod is required
    because every GL-virtual installation, need obviously a different hidden service,
    and the fist access works as "ok setup my hidden service"
    """

    # I'm shae the funny whore!
    if len(settings.globals.hsurl) is 22 and settings.globals.hsurl[0] is not "_":
        configured_hs = True
    else:
        configured_hs = False

    if not configured_hs and settings.globals.under_installation:
        return lambda: redirect('/globaleaks/installation/hidden_service_error.html')

    if not configured_hs and not settings.globals.under_installation:
        return lambda: redirect('/globaleaks/installation/start_setup.html')

    admin_row = db(db.auth_user.username == 'admin').select().first()

    if not admin_row: 
        return lambda: redirect('/globaleaks/installation/virtual_setup.html')

    return funct
