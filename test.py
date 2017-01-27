#!/usr/bin/env python

from ubcmhn.bootstrap import config
from ubcmhn.model import DbEngine
from ubcmhn.controllers.hackernews import HackerNewsDataFetchController

from hackernews import HackerNews

# task test
from ubcmhn.celeryapp.tasks.debug.tasks import hello

# Raw DB
db = DbEngine(config)
#db.dropdb()

# BaseController Test (Db ok?)
#x = HackerNewsDataFetchController(config)

#x.updateVisibleTopStories()
#hn = HackerNews()

#p = db.get_visiblestorylist()
#i = p['itemlist']


from ubcmhn.util.hnwrappers import HnWrappedItem

#r = HnWrappedItem(hn.get_item(i[0]))
#x2 = db.insert__wrappeditem(r)

#x.UpdateVisibleTopStories()

#x.FetchVisibleTopStories()

db.deleteall_locks()

from ubcmhn.controllers.mongofunlocks import Lock, MongoFunLockController

l1 = Lock('hell-debug',expireseconds=70)

db.insert_lock(l1)

i = MongoFunLockController(config)



