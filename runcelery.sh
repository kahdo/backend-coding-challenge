#!/bin/bash

# Relative to project root.
CELERYENTRYPOINT="ubcmhn.celeryapp.apprunner"

#Number of concurrent pool workers
CONCURRENCY=4

# Purge stale queue
celery purge -f

# Run celery worker with "beat" enabled and loglevel=info
celery -A $CELERYENTRYPOINT worker -c $CONCURRENCY -B -l info $*
