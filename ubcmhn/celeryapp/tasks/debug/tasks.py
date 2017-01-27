from ubcmhn.celeryapp.app import celeryapp
import time
import sys

from ubcmhn.config.getconfig import config
from ubcmhn.controllers.mongofunlocks import MongoFunLock



@celeryapp.task(ignore_result=True)
@MongoFunLock(config, 'hell-debug', expireseconds=70)
def hello():
    print("entered hello")
    time.sleep(30)
    print("time has passed!!")
    sys.stdout.flush()
