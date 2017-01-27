from hackernews import Item
import datetime

Item

class HnWrappedItem:
    """
    Simple wrapper to make it easier to clean/input HN Item data to the DB and also
    change/add some attributes that are going to be needed in the translation process.
    """
    def __init__(self, item : Item, status="new"):
        self.__item = item

        self.creation_time = datetime.datetime.utcnow()
        self.itemstatus = status

    def from_json(self, jsondata):
        self.__item = Item(jsondata)

    def dict(self):
        # Get all attributes that don"t start with __
        rv = dict(self.__item.__dict__)

        # Strip unwanted keys, like the raw json response.
        removekeys = ('raw',)
        for rk in removekeys:
            if rk in rv:
                del rv[rk]

        # Add some more fields
        rv['creation_time'] = self.creation_time
        rv['itemstatus'] = self.itemstatus

        return rv

    def __getattr__(self, name):
        return getattr(self.__item, name)


