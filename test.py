#!/usr/bin/env python

from ubcmhn.bootstrap import config
from ubcmhn.model import DbEngine
from ubcmhn.controllers.base import BaseController

# Raw DB
db = DbEngine(config)
db.dropdb()

objid = db.insert_item({"blah": "bloh"})

# BaseController Test (Db ok?)
x = BaseController(config)