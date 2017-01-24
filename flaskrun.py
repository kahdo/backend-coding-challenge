#!/usr/bin/env python

# Bootstrap the application's log facilities and get the config object (folders, dbpaths, etc).
import ubcmhn.bootstrap
import logging

##########################################
# Load Flask WSGI application
##########################################
from ubcmhn.flaskapp.app import app

##########################################
# Dev? Run it.
##########################################
if __name__ == '__main__':
    l = logging.getLogger("UnbabelChallengeMultilingualHackerNews Standalone Runner")
    l.info("Running APP from __main__...")
    # Run and serve via Flask's Built-In HTTP Server
    app.run()