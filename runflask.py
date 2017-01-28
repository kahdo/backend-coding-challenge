#!/usr/bin/env python

# Bootstrap the application's log facilities and get the config object (folders, dbpaths, etc).
import ubcmhn.bootstrap
import logging

##########################################
# Load Flask WSGI application
##########################################
from ubcmhn.flaskapp.app import flaskapp

##########################################
# Dev? Run it.
##########################################
if __name__ == '__main__':
    l = logging.getLogger("UBCMHN Standalone Runner")
    l.info("Running APP from __main__...")
    # Run and serve via Flask's Built-In HTTP Server
    flaskapp.run(host="0.0.0.0")
