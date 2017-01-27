import datetime

import pymongo
from bson.objectid import ObjectId

from hackernews import HackerNews

from ubcmhn.controllers.base import BaseController
from ubcmhn.util.hnwrappers import HnWrappedItem


class HackerNewsDataFetchController(BaseController):
    def init(self):
        self.hn = HackerNews()

    def UpdateVisibleTopStories(self, _count=10):
        l = self.l()
        hn = self.hn
        db = self.db

        # Get storylist
        storylist = hn.top_stories(_count)

        # Generate db document
        visiblestorylist = {
            'itemlist' : storylist,
            'gentime' : datetime.datetime.utcnow()

        }

        insertid = self.db.insert_visiblestorylist(visiblestorylist)

        l.info("Updated visible story list...")

        return visiblestorylist['itemlist']

    def StoreOrUpdateBasicItemData(self, wrappeditem : HnWrappedItem):

        # Get dict from wrappeditem.
        wrappeddict = wrappeditem.dict()

        # Item exists?
        dbitem = self.db.get_itembyhnid(wrappeddict.get('item_id'))

        if dbitem:
            # Upsert
            self.l().warning("Updating HN Item ID {0}...".format(wrappeddict['item_id']))

            # Update dbitem with some of datad's fields.
            updateablefields = ('title','url','text','score','kids','deleted','dead')
            for keyname in updateablefields:

                # TODO: Remove this, for initial dev and amusement only :)
                if wrappeddict.get(keyname) != dbitem[keyname]:
                    self.l().warning("[HN={0}] Updating field {1}...".format(wrappeddict['item_id'],keyname))

                dbitem[keyname] = wrappeddict.get(keyname)

            # Do upsert
            self.db.upsert_item(dbitem)

            # Return the same (unchanged) objid
            return dbitem['_id']
        else:
            # Insert
            self.l().warning("New HN Item ID {0}...".format(wrappeddict['item_id']))

            # Insert and return the new item's objid
            return self.db.insert_wrappeditem(wrappeditem)

    def FetchHnItemDataByHnItemId(self, hnitemid):
        hn = self.hn
        self.l().info("Processing HN Item ID={0}".format(hnitemid))

        item = hn.get_item(hnitemid)
        wrappeditem = HnWrappedItem(item)

        return self.StoreOrUpdateBasicItemData(wrappeditem)

    def FetchHnItemKidsByObjId(self, objid_str, depth=0):

        item = self.db.get_itembyobjid(ObjectId(objid_str))

        kids = item['kids'] if item['kids'] else []

        if kids:
            self.l().info("[HN={0}] {1} kids | depth {0}".format(item['item_id'],len(kids), depth))

        return_kid_objectids = []
        for kid_id in kids:

            # Fetch Kid
            kid_objid = self.FetchHnItemDataByHnItemId(kid_id)

            # Append str(ObjectId) and return that
            return_kid_objectids.append(str(kid_objid))

            self.l().warning("[HN={0}] Kid HN={1} | Recursive fetch | DEP({2})".format(item['item_id'],
                                                                                        kid_id,
                                                                                        depth))

        return return_kid_objectids
