#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

if '__file__' in globals():
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
else:
    path = os.getcwd() # Seems necessary for py2exe

sys.path = [path]+[p for p in sys.path if not p==path]

# import gluon.import_all ##### This should be uncommented for py2exe.py
import gluon.widget

gluon.widget.ProgramName="Open Source Whistleblowing Framework"
gluon.widget.ProgramAuthor="Created by Random GlobaLeaks Developers"
gluon.widget.ProgramVersion="version 0.0000"
gluon.widget.ProgramInfo="Starting up..."

# Start Web2py and Web2py cron service!
gluon.widget.start(cron=True)

