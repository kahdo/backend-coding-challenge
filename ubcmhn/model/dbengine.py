import datetime
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

    @mongodbmethod
    def get_allitems(self, dbo : Database) -> HnWrappedItem:
        items = dbo["items"]
        return items.find({})

    # Translation X Items
    @mongodbmethod
    def get_untranslated_comments(self, dbo : Database, targetlang, exists=False):
        items = dbo["items"]

        attrname = "text_{0}".format(targetlang)

        # Return list of untranslated COMMENTS in that language
        return items.find({"item_type": "comment", attrname : {"$exists": exists}})

    @mongodbmethod
    def get_translated_comments(self, dbo : Database, targetlang):
        return self.get_untranslated_comments(targetlang, exists=True)

    @mongodbmethod
    def get_untranslated_stories(self, dbo : Database, targetlang, exists=False):
        items = dbo["items"]

        attrname = "title_{0}".format(targetlang)

        # Return list of untranslated STORIES in that language
        return items.find({"item_type": "story", attrname : {"$exists": exists}})

    @mongodbmethod
    def get_translated_stories(self, dbo : Database, targetlang):
        return self.get_untranslated_stories(targetlang, exists=True)

    @mongodbmethod
    def get_translationrequested_items(self, dbo : Database, targetlang):
        items = dbo["items"]

        attrname = "unbabeljobid_{0}".format(targetlang)

        return items.find({attrname : {'$exists': True}})

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


    # Task RunLog
    @mongodbmethod
    def logrun(self, dbo: Database, taskname):
        taskruns = dbo['taskruns']

        data = {
            'task' : taskname,
            'time' : datetime.datetime.utcnow()
        }

        return taskruns.insert_one(data).inserted_id

    @mongodbmethod
    def listtaskruns(self, dbo: Database, limit=10):
        taskruns = dbo['taskruns']
        return taskruns.find().sort({ 'time' : DESCENDING}).limit(limit)




# Exported name for the whole system
DbEngine = UbcmhnDbEngine

