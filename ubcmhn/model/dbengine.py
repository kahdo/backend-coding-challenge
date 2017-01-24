from functools import wraps


from bson import ObjectId
from pymongo.database import Database
from .dbenginebase import MongoDbEngineBase


def dbmethod(func):
    """
    Decorator that automatically passes the project's Database Obj as second argument of
    a MongoDbEngineBase (or subclass) instance.

    A simple convenience method to save some time and typing (DRY).
    """
    @wraps(func)
    def decorated_dbengine_method(self : MongoDbEngineBase, *args, **kwargs):
        # Pass the database object as the second argument
        return func(self, self.getdatabase(), *args, **kwargs)
    return decorated_dbengine_method


class UbcmhnDbEngine(MongoDbEngineBase):

    @dbmethod
    def insert_item(self, dbo : Database, item):
        items = dbo["items"]
        return items.insert_one(item).inserted_id

    @dbmethod
    def getitembyid(self, dbo, id_str):
        items = dbo["items"]

        return items.find_one({ '_id' : ObjectId(id_str)})


# Exported name for the whole system
DbEngine = UbcmhnDbEngine

