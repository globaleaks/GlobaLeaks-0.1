GlobaLeaks
==========

GlobaLeaks is the first Open Source Whistleblowing Framework.

It empowers anyone to easily setup and maintain their own Whistleblowing platform. It is also a collection of what are the best practices for people receiveiving and submitting material. GlobaLeaks works in various environments: media, activism, corporations, public agencies.

                                        DISCLAIMER
                                GlobaLeaks it's under Development

Installation
------------------------------------------------------------------

First of all you need to get a copy of web2py, you can install it doing

    pip install web2py

then install Globaleaks

    pip install git+git://github.com/globaleaks/GlobaLeaks.git#egg=globaleaks

under Linux, use the script:
    globaleaks/globaleaks.debian.sh [init.d script]

Under Windows|MacOSX|whatever, start the service with:
    globaleaks/startglobaleaks

then you could found running those web services:

* whistleblowing interface its bind at http://127.0.0.1:8000
* node administrator targets configuratation http://127.0.0.1:8000/globaleaks/admin/
* debug only global view interface: http://127.0.0.1:8000/globalview
* web2py developer access: http://127.0.0.1:8000/admin password "globaleaks"

How to hack on it
-----------------

* You need to get a copy of [web2py](http://www.web2py.com/) and install it (that means get the necessary gluons into $PYTHON_PATH)
* You need to know the MVC programming model, and the [web2py framework documentation](http://web2py.com/book).
* Read & understand the issue list https://github.com/globaleaks/GlobaLeaks/issues
* When globaleaks is running, you could check the reachable pages, this is the expanded list get from routes.py:
1. http://127.0.0.1:8000/globalview
2. http://127.0.0.1:8000/tulip
3. http://127.0.0.1:8000/targets
4. http://127.0.0.1:8000/submit
5. http://127.0.0.1:8000/subscribe
6. http://127.0.0.1:8000/unsubscribe
7. http://127.0.0.1:8000/groups

You are invited to develop, using the web admin interface, because apply automatic checks before saving the code.

updated link-o-graphy
---------------------

* [GlobaLeaks website](http://www.globaleaks.org)
* [code repository](https://github.com/globaleaks)
* [GL's blogroll](http://planet.globaleaks.org)
* [mailing list "people"](http://box549.bluehost.com/mailman/listinfo/people_globaleaks.org)
* [GL's twitter](https://twitter.com/#!/globaleaks)
* [GlobaLeaks documentation](https://github.com/globaleaks/advocacy)

eldest pages reference, documentation
-------------------------------------

* [launchpad old project page](https://launchpad.net/globaleaks)
* [old list of features](https://blueprints.launchpad.net/globaleaks)
* [old site, old ideas, old goals](http://www.globaleaks.org/old/)
* [old trac, old ideas, old goals](http://sourceforge.net/apps/trac/globaleaks/)

GlobaLeaks hackathon soundtrack
-------------------------------

* [Enter the Ninja](http://www.youtube.com/watch?v=cegdR0GiJl4)
* the Target's lament: [don't make me a target](http://www.youtube.com/watch?v=CBtXw6CPwg4)

