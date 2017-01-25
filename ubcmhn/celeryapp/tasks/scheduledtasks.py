from celery import Celery
from celery.schedules import crontab
from ubcmhn.celeryapp.app import celeryapp


# Pull tasks we want to schedule.
from .debug.tasks import hello

@celeryapp.on_after_configure.connect
def setup_scheduled_tasks(sender : Celery, **kwargs):

    #Every 20 seconds
    sender.add_periodic_task(20, hello.s(), name="call hello 20s")