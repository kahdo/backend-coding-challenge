import os
import logging
from .configloader import CfgClass

# Load config or die.
def get_config_or_die(envvar="UBCMHNCFG", defaultcfgname="devel") -> CfgClass:
    l = logging.getLogger("get_config_or_die")
    try:
        # Get config name
        cfgname = defaultcfgname
        if envvar in os.environ:
            # Override wanted config name
            cfgname = os.environ[envvar]
        l.debug("Trying to load config \"{0}\"...".format(cfgname))

        # Try to return ConfigLoader
        return CfgClass(cfgname)
    except:
        l.critical("Could not open config")
        raise
        exit(1)


# Get the actual config.
config = get_config_or_die()