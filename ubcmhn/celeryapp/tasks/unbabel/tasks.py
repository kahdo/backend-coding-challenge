from ubcmhn.config.getconfig import config

from ubcmhn.controllers.unbabel import UnbabelTranslationController
from ubcmhn.controllers.mongofunlocks import MongoFunLock

from celery import group
from ubcmhn.celeryapp.app import celeryapp


#############
# MAIN ENTRY POINT
#############
@celeryapp.task(ignore_result=True)
@MongoFunLock(config, 'request_allitem_translation', expireseconds=600)
def request_allitem_translation():

    cnt = UnbabelTranslationController(config)

    rv = cnt.FindUntranslatedItems()

    # Assemble one HUGE list of tasks to run in parallel, and WAIT for their completion
    tasklist = []
    for targetlang in rv:

        stories, comments = rv[targetlang]
        allitems = stories + comments

        for story in allitems:
            print("requesting translation for {1} item_id = {0}".format(story['item_id'],
                                                                        story['item_type']))
            tasklist.append(translate_one_item.s(story['item_id'], targetlang))

    # Run the tasklist as a celery-group. wait for completion
    tasklist_group = group(tasklist)
    tasklist_group.apply()

    cnt.db.logrun(request_allitem_translation.__name__)

@celeryapp.task(ignore_result=True)
def translate_one_item(hnitem_id, targetlang : str):

    print("Requesting Translation HN={0} to \"{1}\"...".format(hnitem_id, targetlang.upper()))
    cnt = UnbabelTranslationController(config)
    cnt.RequestTranslation(hnitem_id, targetlang)

#############
# MAIN ENTRY POINT
#############
@celeryapp.task(ignore_result=True)
@MongoFunLock(config, 'fetch_all_processedtranslations', expireseconds=600)
def fetch_all_processedtranslations():

    cnt = UnbabelTranslationController(config)
    rv = cnt.FindRequestedTranslations()

    # Assemble one HUGE list of tasks to run in parallel, and WAIT for their completion
    tasklist = []
    for targetlang in rv:

        items = rv[targetlang]

        for item in items:
            print("fetching translation job for {1} item_id = {0}".format(item['item_id'],
                                                                          item['item_type']))
            tasklist.append(fetch_one_translated_item.s(item['item_id'], targetlang))

    # Run the tasklist as a celery-group. wait for completion
    tasklist_group = group(tasklist)
    tasklist_group.apply()


@celeryapp.task(ignore_result=True)
def fetch_one_translated_item(hnitem_id, targetlang: str):

    print("Requesting Translation HN={0} to \"{1}\"...".format(hnitem_id, targetlang.upper()))
    cnt = UnbabelTranslationController(config)
    cnt.FetchTranslation(hnitem_id, targetlang)