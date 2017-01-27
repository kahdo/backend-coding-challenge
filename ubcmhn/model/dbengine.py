from bson import ObjectId
from pymongo.database import Database
from pymongo import ASCENDING, DESCENDING
from ubcmhn.util.hnwrappers import HnWrappedItem
from .dbenginebase import MongoDbEngineBase,mongodbmethod


class UbcmhnDbEngine(MongoDbEngineBase):

    # Visible Story List
    # The list of all stories that will be shown at any given time.
    # Gets updated from time to time and stories get pushed out of exhibit.
    @mongodbmethod
    def insert_visiblestorylist(self, dbo : Database, item):
        vsl = dbo["visiblestorylist"]
        return vsl.insert_one(item).inserted_id

    @mongodbmethod
    def get_visiblestorylist(self, dbo : Database):
        """ Returns the list of stories that should be shown in our ML clone"""

        vsl = dbo["visiblestorylist"]

        data = [x for x in vsl.find()
                             .sort('gentime', DESCENDING)
                             .limit(1)]

        if data:
            return data[0]

    # HNWrappedItem (and normal Items, already in the Collection)
    # Akin to HackerNews 'item' data type
    @mongodbmethod
    def insert_wrappeditem(self, dbo : Database, wrappeditem : HnWrappedItem):
        items = dbo["items"]
        return items.insert_one(wrappeditem.dict()).inserted_id

    @mongodbmethod
    def upsert_item(self, dbo : Database, item):
        items = dbo["items"]
        return items.replace_one({'_id' : item['_id']}, item, upsert=True)

    @mongodbmethod
    def get_itembyobjid(self, dbo : Database, objid_str) -> HnWrappedItem:
        items = dbo["items"]

        return items.find_one({'_id' : ObjectId(objid_str)})

    @mongodbmethod
    def get_itembyhnid(self, dbo : Database, hackernews_id):
        items = dbo["items"]

        return items.find_one({'item_id' : hackernews_id})

    # Function Locks
    # (Ex.: to avoid having scheduled/parallel funcs overlap over themselves, trashing)
    @mongodbmethod
    def deleteall_locks(self, dbo: Database) -> int:
        locks = dbo['locks']
        return locks.delete_many({}).deleted_count

    @mongodbmethod
    def get_lockbyname(self, dbo : Database, lockname):
        locks = dbo['locks']
        return locks.find_one({'lockname' : lockname})

    @mongodbmethod
    def insert_lock(self, dbo : Database, lockdata) -> ObjectId:
        locks = dbo['locks']

        # Lock exists? Abort
        lockitem = self.get_lockbyname(lockdata['lockname'])
        if lockitem:
            return

        # Create Lock
        return locks.insert_one(lockdata).inserted_id

    @mongodbmethod
    def delete_lockbyname(self, dbo: Database, lockname) -> int:
        locks = dbo['locks']
        return locks.delete_many({'lockname' : lockname}).deleted_count






# Exported name for the whole system
DbEngine = UbcmhnDbEngine

