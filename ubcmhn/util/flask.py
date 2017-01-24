from typing import List
from functools import wraps
from urllib.parse import urlsplit
import datetime
import os

from ubcmhn.util.json import dumpjson
from ubcmhn.util.dataload import module2list

from flask import Blueprint, request, Request

# Dynamically get all blueprints.
def get_blueprints_from( _module) -> List[Blueprint]:
    """
    Get all instances of Blueprint out of a module
    Used to get all blueprints dynamically from the "views" module
    """
    return filter(lambda o: isinstance(o, Blueprint), module2list(_module))

## getrequest()
## Makes the return request proxy obj autocomplete properly on IDEs
def get_request() -> Request:
    return request

# Decorator to be applied in view functions to save the incoming request data to a folder
# Useful for debugging/form study purposes
def save_request_data(folder="reqs/", ext="json"):

    def decorator_wrapper(f):

        @wraps(f)
        def real_decorator(*args, **kwargs):
            # Get request.

            r = get_request()

            #Filename
            now = datetime.datetime.now()
            fname = "{0}{1:02}{2:02}_{3:02}{4:02}{5:02}.{6}".format(now.year, now.month, now.day,
                                                                  now.hour, now.minute, now.second, ext)

            # Url Path - Discard first char ("/")
            urlpath = urlsplit(r.url).path[1:]

            # Assemble dirpath from url
            dirpath = os.path.join(folder, urlpath)

            filepath = os.path.join(dirpath, fname)

            # Create folders
            if not os.path.isdir(dirpath):
                os.makedirs(dirpath)

            # Write file
            with open(filepath, 'wb') as fileobj:
                if r.json:
                    fileobj.write(bytes(dumpjson(r.json),'utf8'))
                else:
                    fileobj.write(r.data)

                print("###")
                print("#### Request data saved to {0}".format(filepath))
                print("###")

            # Run the original view function and return its value.
            return f(*args, **kwargs)

        return real_decorator

    return decorator_wrapper

