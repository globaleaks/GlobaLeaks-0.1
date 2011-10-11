# General configuration
The first place where you should look for customization is the GlobaLeaks config file.
It is located in globaleaks/applications/globaleaks/models/gleaks.cfg.
From here you are able to set the following parameters:
    [global]
    title = <the title of your site>
    subtitle = <subtitle>
    author = <author>
    description = <description of site>
    disclaimer = <submission page disclaimer>
    layout_theme = Default
    author_email = <email address of site maintainer>

    # must be changed to random string
    security_key = CHANGEMEPLEASETOARANDOMSTRINGOFCHARSNUMBERS
    email_server =
    email_sender = node@globaleaks.org
    email_login =
    login_method =
    login_config =

    [tulip]
    max_access = 1
    expire = 2

    [logging]
    server = True
    client = True
    logfile = /tmp/globaleaks.log

    [database]
    uri = sqlite://storage.sqlite

# Presentation
For customizing the look of your site you should be looking at globaleaks/applications/globaleaks/views/.
layout.html - Contains the main layout included in every page
    * For customizing the logo in every page look for "header" and replace the image with your own logo.

inside globaleaks/applications/globaleaks/static you will find all the .css files. The main css file is base.css.


