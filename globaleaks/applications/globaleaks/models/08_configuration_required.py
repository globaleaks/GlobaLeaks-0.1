def configuration_required:
    """
    This function is called ahead of every controller function that
    require to run in a proper configured GlobaLeaks environment.
    Is checked the presence of the administrative_password, unset in the 
    default, as configuration trigger
    """

    if not settings.global.admin_password:
        response.flash = "The requested utility required a minimum configuration in your GlobaLeaks node"
        redirect('globaleaks/installation/configuration.html')
    
