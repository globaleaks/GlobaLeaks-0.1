def configuration_required(funct):
    """
    This function is called ahead of every controller function that
    require to run in a proper configured GlobaLeaks environment.
    Is checked the presence of the node_admin_configured, set as true
    when the mandatory configuartion is provieded
    """

    if not settings['globals'].node_admin_configured:
        return lambda: redirect('/globaleaks/installation/mandatory_setup.html')
#        return lambda: redirect('/globaleaks/admin/wizard')
    else:
        return funct
