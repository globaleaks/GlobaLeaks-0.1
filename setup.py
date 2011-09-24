#!/usr/bin/env python

from distutils.core import setup
from glob import glob


packages = ['applications',
            '']

setup(name='Globaleaks',
      version='0.hackathon',
      description='A flexible Opensource Whistleblowing Platform',
      author='Random Globaleaks Developers',
      url='http://www.globaleaks.org/',
      requires=['gluon']
      packages=packages,

     )
