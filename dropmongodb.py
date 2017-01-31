#!/usr/bin/env python

from ubcmhn.bootstrap import config
from ubcmhn.model import DbEngine
# Raw DB
print("Dropping DB")
db = DbEngine(config)
db.dropdb()
