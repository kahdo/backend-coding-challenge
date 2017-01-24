from celery import Celery
import time

app = Celery('hello', backend='rpc://', broker='amqp://guest@localhost//')

@app.task
def hello():
    time.sleep(10)
    return 'hello world'


@app.task
def helloarg(arg):
    time.sleep(10)
    return 'hello world [{0}]'.format(arg)