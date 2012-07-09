def configuration_required(funct):
    """
    This function is called ahead of every controller function that
    require to run in a proper configured GlobaLeaks environment.
    """

    if settings.globals.under_installation:
        return lambda: redirect('/globaleaks/installation/password_setup.html')

    return funct
