from __future__ import absolute_import
from .celery import app
from celery.utils.log import get_task_logger
from .RedisQueue import RedisQueue
import time
import json
import requests

logger = get_task_logger(__name__)
q = RedisQueue('test')

@app.task(bind=True)
def celpost(self, argument, rdata):
    logger.info('celpost {0} + {1}'.format(argument, rdata))
    res=requests.post(argument, json=rdata)
    #once result is ready then process
    #update db?
    #send location URL
    print(res)
    return "Done"

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task(bind=True)
def basic_celery_task(self):
    #time.sleep(5) 
    self.job = call_within_call.delay(str(q.get() ) )
    #print (self.job.get() )

    # Loops infite to get the next element in the queue and calls other task  
    #while True:
        #if self.job.state == 'SUCCESS':
            #self.job = call_within_call.delay(str(q.get()))
            #print (self.job.get() )
    #        print("We are this far")
    return 'True'


# This task accepts input from basic_celery_task and works on it. 
@app.task(bind=True)
def call_within_call(self,arg):
    # call the MC with URI
    time.sleep(5)
    return arg + 'Completed'

