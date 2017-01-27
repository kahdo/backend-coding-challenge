#!/usr/bin/env python

from ubcmhn.bootstrap import config
from ubcmhn.model import DbEngine

from hackernews import HackerNews

# task test
from ubcmhn.celeryapp.tasks.debug.tasks import hello

# Raw DB
print("Dropping DB")
db = DbEngine(config)
db.dropdb()
