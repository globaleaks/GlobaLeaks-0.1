========
Tutorial
========
This tutorial is intended to help developers dowload and build
GlobaLeaks from scratch. After downloading and building ANTANII

.. note:: Stable dowloads for PC/Mac/Linux are avaible in the `download`_
          page.


Download
--------

GlobaLeaks depends on `web2py`_, which can be downloaded using pip ::
    $ sudo pip install web2py

    $ sudo  easy_install web2py

Download the lastest rev of GlobaLeaks from `GitHub`_ using git: ::

    $ git clone git://github.com/globaleaks/GlobaLeaks.git

Then cd- into `GlobaLeaks/` ::
    $ cd GlobaLeaks/

Run
---
To run web2py http server, simply type ::

    $ ./startglobaleaks

Http applciation is avaible at `localhost`_ .


Install
-------
Since GlobaLeaks aims to provide a light, portable whistleblowing platform, it's
not necessary to install it. However, you can easily install it ::


    $ sudo python setup.py install

That's all folks!



.. _download: http://google.com
.. _GitHub: https://github.com/globaleaks/GlobaLeaks
.. _localhost: http://127.0.0.1:8000/
.. _web2py: http://web2py.com/
