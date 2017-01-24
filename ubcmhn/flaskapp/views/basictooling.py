# Each view needs these basic objects.

# - App Config - Instantiated
from ubcmhn.config.getconfig import config

# - View URL Prefix Function - From Config.URLPREFIX
# Example:
# If URLPREFIX is "/api" the Blueprint's url_prefix becomes "/api/<url>"
import posixpath
def make_urlprefix(urlprefix):
    return posixpath.join(config.URLPREFIX, urlprefix)
