#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
import globaleaks

setup(name=globaleaks.__name__,
      version=globaleaks.__version__,
      description='The Opensource Whistleblowing Framework',
      author=globaleaks.__authors__,
      author_email=globaleaks.__mail__,
      url=globaleaks.__site__,
      #install_requires=['web2py'],
      packages=find_packages(),
      zip_safe=False,
      extras_require = {},
      entry_points="""
      """,
      include_package_data=True,
      scripts=['globaleaks/startglobaleaks'],
     )
