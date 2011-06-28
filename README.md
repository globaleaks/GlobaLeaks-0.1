# What is GlobaLeaks?

GlobaLeaks is an open source project aimed to create a worldwide,
anonymous, censorship-resistant, distributed Leak Amplification
Network supporting whistleblowers all around the world.

GlobaLeaks is a Leak Amplification Platform to allow the Leaks
to get delivered to the right public media, mainly for what's
related to a city, region, country or even corporation level.

# Technical Requirements
### Self Contained:
The software must be self-contained and not depend on third party
services other than Tor (no mysql or apache installation). 
### Web based:
The software will be used entirely trough a web browser. A web interface
will be provided to whistleblowers, targets and node maintainers.
### Easy to be installed:
The software must be easy to instal and manage by non-technical people.
An executable for Windows, App for OSX, Debian Package for Linux.
### Cross Platform:
The software must be cross-platform in order to setup and run a server on workstations
such as Windows, Mac OS X or Linux.
### Open Source:
The software must be open source in order to allow community based growth of the
software project.
### Network Agnostic:
The system must be Network Agnostic, not requiring domains, dedicated ip addreses
to run.

# Technology selection

* Language: Python
* Web Server: Twisted
* Web Framework: Nevow + Athena
* Database: SQLite
* SMTPS Client: Twisted
* Build: Windows/Py2exe - OSX/Py2app - Linux/Debian