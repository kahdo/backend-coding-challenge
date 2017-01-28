from functools import wraps
import time

import datetime
import json

from ubcmhn.controllers.base import BaseController
from ubcmhn.util.hnwrappers import TrFieldsByHnItem, ItemTranslationStatus

def strip_objid(mdict : dict):
    if mdict.get("_id"):
        del mdict["_id"]
    return mdict

class DataPresentationController(BaseController):

    def GetLanguages(self):
        # TODO: this should be dynamic, but since this is a toy project and we're late ;-)
        return (self.config.SRCLANG, self.config.DSTLANG1, self.config.DSTLANG2)

    def monkey_patch_translation(self, _hnitem, language):
        hnitem = dict(_hnitem)
        if not (language == self.config.SRCLANG):
            # Different language, monkey-patch translated text in

            trstatus = ItemTranslationStatus(hnitem, language)
            orig, trf, ubj = TrFieldsByHnItem(hnitem, language)

            unbabeljobstatus = "N/A"
            if hnitem.get(ubj):
                unbabeljobstatus = hnitem[ubj]['status']

            realtitle = hnitem.get(trf) if hnitem.get(trf) else hnitem.get(orig)

            itemstatus = ""

            if trstatus != "translated":
                itemstatus = " (LANG:{} STATUS:{} UB_JOBSTATUS:{})".format(
                    language,
                    trstatus,
                    unbabeljobstatus)

            t = "{0}{1}".format(
                realtitle,
                itemstatus)

            hnitem[orig] = t

        return hnitem


    def GetIndexPageData(self, language='en') -> bool:

        vsl = self.db.get_visiblestorylist()

        itemlist = vsl['itemlist']

        rv = []

        for itemid in itemlist:
            hnitem = self.db.get_itembyhnid(itemid)
            processed_hnitem = self.monkey_patch_translation(hnitem, language)
            rv.append(strip_objid(processed_hnitem))

        return rv

    def GetStoryCommentData(self, itemid, language='en'):

        print("itemid -> {}".format(itemid))

        hnstory = self.db.get_itembyhnid(itemid)
        if not hnstory:
            return
        if hnstory['item_type'] != 'story':
            return

        trhnstory = self.monkey_patch_translation(hnstory, language)

        def getallkids_aslist(rootitem : dict, depth=0):
            rv = []

            kids = rootitem.get("kids")
            if not kids:
                return []

            for kidid in kids:
                kiditem = self.db.get_itembyhnid(kidid)

                if not kiditem:
                    self.l().info("Skipping BLANK HNITEMID={}".format(kidid))
                    continue

                self.l().info("Processing HNITEMID={}".format(kidid))

                # Monkey patch the language
                tr_kiditem = self.monkey_patch_translation(kiditem, language)

                # Assemble and add (comment depth, comment data)
                kiddata = (depth, tr_kiditem)
                rv.append(kiddata)

                # Recursively do the same thing to the kids' kids....
                kids_kids = kiditem.get("kids")
                if kids_kids:
                    newdepth = depth +1
                    rv = rv + getallkids_aslist(kiditem, depth=newdepth)

            return rv

        return (trhnstory, getallkids_aslist(hnstory))