from hello import hello
import time

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

# run it
x = hello.delay()

a=0
while True:
    if x.ready() == True:
        break
    else:
        sys.stdout.write("{0};".format(a))
        a+=1
        time.sleep(1)
sys.stdout.write("")

sys.stdout.write("Result -> {0}\n".format(x.get()))




