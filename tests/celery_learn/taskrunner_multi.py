from time import sleep
from hello import helloarg

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)


# How many tasks to run
amount = 10

# Run 10 tasks
taskpool = [helloarg.delay(x) for x in range(amount)]

# While there are tasks which ready==False
donetasks = lambda : sum([x.ready() for x in taskpool if x.ready() == True])

while donetasks() != amount:
    sys.stdout.write(".")
    sleep(0.5)

print("[Getting results]")
for promise in taskpool:
    print("Result: {0}".format(promise.result))
