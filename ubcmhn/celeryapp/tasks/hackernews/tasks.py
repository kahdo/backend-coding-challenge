from ubcmhn.config.getconfig import config
import time
from celery import group
from ubcmhn.celeryapp.app import celeryapp

from ubcmhn.controllers.hackernews import HackerNewsDataFetchController
from ubcmhn.controllers.mongofunlocks import MongoFunLock

#############
# MAIN ENTRY POINT
# - Update visible stories (top 10 'hot' stories)
# - Call subtask to update the stories kids recursively (items can be edited, deleted, etc)
#############
@celeryapp.task(ignore_result=True)
@MongoFunLock(config, 'get_visible_top_stories_list', expireseconds=600)
def get_visible_top_stories_list():

    cnt = HackerNewsDataFetchController(config)
    storyids = cnt.UpdateVisibleTopStories()
    print("Visible Story List Updated")

    # Update visible top stories in parallel.
    print("Getting Visible Stories Items....")
    tasklist = []
    for storyid in storyids:
        tasklist.append(fetch_hnitem_data_by_hnitemid.s(storyid))

    tasklist_group = group(tasklist)
    # Run it and block until group finishes!
    print("get_visible_top_stories_list:3");    time.sleep(1)
    print("get_visible_top_stories_list:2");    time.sleep(1)
    print("get_visible_top_stories_list:1");    time.sleep(1)
    print("get_visible_top_stories_list:GO!")
    tasklist_group.apply()


@celeryapp.task(ignore_result=True)
def fetch_hnitem_data_by_hnitemid(hnitemid):
    """Update this item's Hacker News related attributes"""
    cnt = HackerNewsDataFetchController(config)

    # Fetch Item and ...
    itemobjid = cnt.FetchHnItemDataByHnItemId(hnitemid)

    # ... all kids
    time.sleep(1)
    fetch_hnitem_kids_by_objid.delay(str(itemobjid))


@celeryapp.task(ignore_result=True)
def fetch_hnitem_kids_by_objid(objid_str, depth=0):
    cnt = HackerNewsDataFetchController(config)

    kid_objids = cnt.FetchHnItemKidsByObjId(objid_str, depth=depth)

    # We must go deeper!
    newdepth = depth + 1
    # Get each kids' kids and so on....
    for kidobjid in kid_objids:
        fetch_hnitem_kids_by_objid.delay(kidobjid, depth=newdepth)
