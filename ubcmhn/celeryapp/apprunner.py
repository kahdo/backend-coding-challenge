# This file is the entry point used in "celery -A <this> worker -B -l info"

# Bootstrap the application's log facilities and get the config object (folders, dbpaths, etc).
import ubcmhn.bootstrap

##########################################
# Load Celery App application
##########################################
from ubcmhn.celeryapp.app import celeryapp

##########################################
# Load Celery Tasks and configure Scheduled Tasks
##########################################
import ubcmhn.celeryapp.tasks
import ubcmhn.celeryapp.tasks.scheduledtasks
