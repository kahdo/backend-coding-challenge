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
from ubcmhn.controllers.unbabel import UnbabelTranslationController

l1 = Lock('hell-debug',expireseconds=70)

db.insert_lock(l1)

i = MongoFunLockController(config)


from ubcmhn.util.unbabelsimpleapi import UnbabelSimpleApi

#api = UnbabelApi("backendchallenge", "711b8090e84dcb4981e6381b59757ac5c75ebb26", sandbox=True)

api = UnbabelSimpleApi("backendchallenge", "711b8090e84dcb4981e6381b59757ac5c75ebb26", sandbox=True)


#o2 = api.post_translation(text="Hello Unbabel, Will you hire me?", source_language="en", target_language="pt")


from ubcmhn.celeryapp.tasks.unbabel.tasks import request_allitem_translation, fetch_all_processedtranslations

#request_allitem_translation()

fetch_all_processedtranslations()

