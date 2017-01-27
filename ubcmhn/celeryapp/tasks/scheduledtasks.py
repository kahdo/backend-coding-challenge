from celery import Celery
from celery.schedules import crontab
from ubcmhn.celeryapp.app import celeryapp


# Pull tasks we want to schedule.
from .debug.tasks import hello
from .hackernews.tasks import get_visible_top_stories_list

@celeryapp.on_after_configure.connect
def setup_scheduled_tasks(sender : Celery, **kwargs):

    #Every 20 seconds
    #sender.add_periodic_task(10, hello.s(), name="call hello 10s")

    # Every 600 seconds update the visible top stories list and the visible items (and kids)
    sender.add_periodic_task(600, get_visible_top_stories_list.s(), name="get_visible_top_stories")