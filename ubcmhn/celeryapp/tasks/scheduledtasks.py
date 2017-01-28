from celery import Celery
from celery.schedules import crontab
from ubcmhn.celeryapp.app import celeryapp


# Pull tasks we want to schedule.
from .debug.tasks import hello
from .hackernews.tasks import get_visible_top_stories_list
from .unbabel.tasks import request_allitem_translation, fetch_all_processedtranslations

@celeryapp.on_after_configure.connect
def setup_scheduled_tasks(sender : Celery, **kwargs):

    # Run Debug Hello World
    #sender.add_periodic_task(10, hello.s(), name="call hello 10s")

    # Update the visible top stories list and the visible items (and kids)
    sender.add_periodic_task(480.0, get_visible_top_stories_list.s(), name="get_visible_top_stories")

    ## Request the translation of all items
    sender.add_periodic_task(480.0, request_allitem_translation.s(), name="request_allitem_translation")

    # Fetch the translation of the items that already update the visible top stories list and the visible items (and kids)
    sender.add_periodic_task(480.0, fetch_all_processedtranslations.s(), name="fetch_all_processedtranslations")
