def configuration_required():
    """
    This function is called ahead of every controller function that
    require to run in a proper configured GlobaLeaks environment.
    Is checked the presence of the node_admin_configured, set as true
    when the mandatory configuartion is provieded
    """

    if not settings['globals'].node_admin_configured:
        redirect('globaleaks/installation/configuration.html')
