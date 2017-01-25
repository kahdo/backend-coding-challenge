from ubcmhn.celeryapp.app import celeryapp
import time
import sys

@celeryapp.task(ignore_result=True)
def hello():
    time.sleep(10)
    print("time has passed!")
    sys.stdout.flush()
