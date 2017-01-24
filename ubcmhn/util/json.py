import json

# This way, the whole project has a consistent JSON reporting behavior.
def dumpjson(data):
    return json.dumps(data, indent=4, sort_keys=True)
