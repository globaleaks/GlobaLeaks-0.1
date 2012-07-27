GlobaLeaks
==========

GlobaLeaks is the first Open Source Whistleblowing Framework.

It empowers anyone to easily setup and maintain their own Whistleblowing platform. It is also a collection of what are the best practices for people receiveiving and submitting material. GlobaLeaks works in various environments: media, activism, corporations, public agencies.

# GlobaLeaks virtual branch

TODO description of how to get the virtual image

This branch is planned to be used with https://github.com/vecna/GL-virtual.git

### common usage interfaces

*  whistleblowing interface binds to http://172.16.254.2:8000
*  node administrator targets configuratation http://172.16.254.2:8000/globaleaks/admin/
*  debug only global view interface: http://172.16.254.2:8000/globalview
*  web2py developer access: http://172.16.254.2:8000/admin password "globaleaks"

Base configuration
------------------

inside

    defaults/origin.globaleaks.conf

there are the configuration file with all the required, optional and mandatory fields that an admin could change.
When globaleaks is started, the request of a controller that require a proper configuration will redirect to the configuration page. The admin provide with the few mandatory information, and the file globaleaks.conf is saved.

When the login is requested to access as node maintainer, the default login is in: node_admin_username = admin@globaleaks.local

The file globaleaks/globaleaks.conf contain your personal configuration: mail server, installation name, and usually don't be shared

### all the interfaces

1. http://172.16.254.2:8000/globalview
2. http://172.16.254.2:8000/tulip
3. http://172.16.254.2:8000/targets
4. http://172.16.254.2:8000/submit
5. http://172.16.254.2:8000/subscribe
6. http://172.16.254.2:8000/unsubscribe
7. http://172.16.254.2:8000/groups

You are invited to develop, using the web admin interface, because apply automatic checks before saving the code.

updated link-o-graphy
---------------------

* [GlobaLeaks website](http://www.globaleaks.org)
* [code repository](https://github.com/globaleaks)
* [GL's blogroll](http://planet.globaleaks.org)
* [mailing list "people"](http://box549.bluehost.com/mailman/listinfo/people_globaleaks.org)
* [GL's twitter](https://twitter.com/#!/globaleaks)
* [GlobaLeaks documentation](https://github.com/globaleaks/advocacy)

GlobaLeaks hackathon soundtrack
-------------------------------

* [Enter the Ninja](http://www.youtube.com/watch?v=cegdR0GiJl4)
* the Target's lament: [don't make me a target](http://www.youtube.com/watch?v=CBtXw6CPwg4)
