#!/usr/bin/env python

from ubcmhn.bootstrap import config
from ubcmhn.model import DbEngine
from ubcmhn.controllers.base import BaseController

# task test
from ubcmhn.celeryapp.tasks.debug.tasks import hello

# Raw DB
db = DbEngine(config)
db.dropdb()

objid = db.insert_item({"blah": "blih"})

# BaseController Test (Db ok?)
x = BaseController(config)


#call task
hello.delay()