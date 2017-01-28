from hackernews import Item
import datetime

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

#######################################
### Item Translation Related Funcs
#######################################

def TrFieldsByHnItem(hnitem: dict, targetlang):
    itemtype = hnitem['item_type']

    origfield = ""
    if itemtype == "story":
        origfield = "title"
    elif itemtype == "comment":
        origfield = "text"
    else:
        raise Exception("HnItem of Unknown Type")

    return ItemTrFieldNames(origfield, targetlang)


def ItemTrFieldNames(origfield, targetlang):
    translatedfield = "{0}_{1}".format(origfield, targetlang)
    unbabeltrjobfield = "unbabeljobid_{0}".format(targetlang)

    return (origfield, translatedfield, unbabeltrjobfield)


def ItemTranslationStatus(hnitem: dict, targetlang: str):
    itemtype = hnitem['item_type']

    def __check(hnitem: dict, targetlang: str, origfield="title"):
        status = "untranslated"

        _ign, translatedfield, unbabeltrjobfield = ItemTrFieldNames(origfield, targetlang)

        if hnitem.get(translatedfield):
            status = "translated"
        elif hnitem.get(unbabeltrjobfield):
            status = "processing"

        return status

    def __story(hnitem: dict, targetlang: str):
        return __check(hnitem, targetlang, "title")

    def __comment(hnitem: dict, targetlang: str):
        return __check(hnitem, targetlang, "text")

    arguments = (hnitem, targetlang)

    if itemtype == "story":
        return __story(*arguments)

    elif itemtype == "comment":
        return __comment(*arguments)

    else:
        return None
