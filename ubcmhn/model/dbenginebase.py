from ubcmhn.config.configloader import CfgClass
from ubcmhn.util.useful_baseclasses import LoggableBase

from pymongo import MongoClient
from pymongo.database import Database


class DbEngineBase(LoggableBase):
    def __init__(self, _config : CfgClass, *_args, **_kwargs):
        # Save app config and args.
        self.config = _config
        self.args = _args
        self.kwargs = _kwargs

        # Run custom init
        self.init()

        # Connect to Db and save connection obj
        self.l().debug("Connecting to db...")
        self.db = self.connect()

    def init(self):
        """Override this to set up custom db-connection related configs"""
        pass

    def connect(self):
        """
        Override this to provide a connection method
        Must return a db-connection-like obj"""
        pass

class MongoDbEngineBase(DbEngineBase):
    def init(self):
        # Extract connection string and database name.
        self.connectionstring = self.config.DBCONNECTSTR
        self.dbname = self.config.DBNAME

    def connect(self) -> MongoClient:
        # Connect to MongoDB via connection string
        return MongoClient(self.connectionstring)

    def getdatabase(self) -> Database:
        return self.db[self.dbname] if self.db else None

    def dropdb(self):
        if self.db:
            return self.getdatabase().command('dropDatabase')

    def __repr__(self):
        return "<{0} | MongoDB:{1} Db:{2}>".format(self.__class__.__name__,
                                                  self.connectionstring,
                                                  self.dbname)

