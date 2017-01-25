# Get APP Config.
from ubcmhn.config.getconfig import config

from celery import Celery

# Create Celery APP
celeryapp = Celery(config.CELERYAPPNAME, backend=config.CELERYBACKEND, broker=config.CELERYBROKER)
