from functools import wraps
import time

import datetime

from ubcmhn.controllers.base import BaseController

def Lock(lockname, expireseconds=10):

    lock_time = datetime.datetime.utcnow()
    expire_time = lock_time + datetime.timedelta(seconds=expireseconds)

    rv = {
        'lockname' : lockname,
        'lock_time': lock_time,
        'expire_time': expire_time
    }

    return rv

class MongoFunLockController(BaseController):

    def acquire_or_die(self, lockname, expireseconds=10, taskname="<taskname>") -> bool:

        new_lockdata = Lock(lockname, expireseconds=expireseconds)

        # Return value.
        lockacquired = False

        if self.db.insert_lock(new_lockdata):
            # Lock inserted successfully!
            lockacquired = True

        else:
            # Lock exists! Get it and check if it is expired.
            existing_lockdata = self.db.get_lockbyname(lockname)

            now = datetime.datetime.utcnow()
            if now > existing_lockdata['expire_time']:
                # Lock is expired, delete it
                self.l().warning("Deleting stale lock \"{0}\". task \"{1}\" will run...".format(
                                                                    ))
                self.db.delete_lockbyname(lockname)

                # Insert new lock
                self.db.insert_lock(new_lockdata)

                lockacquired = True

        return lockacquired

    def release_lock(self, lockname):
        return self.db.delete_lockbyname(lockname)

# Decorator to lock a function until the lock in the db is released.
def MongoFunLock(config, lockname, expireseconds=600, logrun=True):

    def funlock_decorator(fun):

        @wraps(fun)
        def real_funlock_decorator(*args, **kwargs):

            # Controller cannot be instantiated outside of the decorator (ex: in the decorator factory)
            # or it will be instantiated outside of the fork()
            cnt = MongoFunLockController(config)

            # Acquire Lock
            if cnt.acquire_or_die(lockname, expireseconds, fun.__name__):
                # Lock Acquired, call function and then release lock
                try:
                    rv = fun(*args, **kwargs)
                except BaseException as e:
                    cnt.l().error("-------------------------")
                    cnt.l().error("(MongoFunLocks) Error in function!!!", exc_info=e)
                    cnt.l().error("-------------------------")
                    time.sleep(5)
                    rv = None
                finally:
                    # Release Lock
                    cnt.release_lock(lockname)
                    # Log Task Run
                    if logrun:
                        cnt.db.logrun(taskname=fun.__name__)
                    # Return function's original return value.
                    return rv
            else:
                # Can't execute function, lock is in place.
                cnt.l().error("Cannot run task \"{1}\" because lock \"{0}\" is active.".format(lockname,
                                                                                             fun.__name__))

        return real_funlock_decorator

    return funlock_decorator


