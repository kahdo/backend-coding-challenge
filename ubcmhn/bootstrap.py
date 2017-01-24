# Start a rudimentary log system.
from ubcmhn.util.logging import bootstrap_logging, configure_logging_from_config
bootstrap_logging()

# Get config object.
from ubcmhn.config.getconfig import config

# Configure real logging, based on ConfigLoader
configure_logging_from_config(config)