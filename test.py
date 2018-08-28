from proj import tasks
from flask import Flask
from flask import request, Response
import json
import os, re
from proj.RedisQueue import RedisQueue
import requests
import time


flask_app = Flask(__name__)

# Example URL to stop the current celery task
@flask_app.route("/terminate",methods=['GET'])
def rfGetVersions():
    result.revoke(terminate=True)
    return("Celery task Terminated")        

@flask_app.route("/tests/endpoint",methods=['POST'])
def rfPostTest():
    print("rfPostTest: POST /tests/endpoint hit")
    rdata=request.get_json(cache=True)
    print ("rfPostTest: We got it %s " % rdata)        
    rdata['sendTestEvent']="Alert recieved you're a liar"
    resp=Response(json.dumps(rdata), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@flask_app.route("/sendTestEvent",methods=['GET'])
def rfSendEvents():
    rdata={'sendTestEvent': "Alert: Pants on fire!"}
    print("sendEvents: GET /sendTestEvent hit")
    print("sendEvents: Now send POST to subscriper")
    #res=requests.post('http://localhost:5001/tests/endpoint', json=rdata)
    tcall=tasks.celpost.delay('http://localhost:5001/tests/endpoint',rdata)
    task=tasks.celpost.AsyncResult(tcall.id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    r=None
    while not r=='SUCCESS':
        r=task.state
        print("state %s" % r)
        time.sleep(0.4)
    print("sendEvents: response %s" % response)
    #print("sendEvents: response from server %s" % res)
    #print("sendEvents: json response %s" % res.json())
    return "Got response"


def _test(argument):
    return "TEST: %s" % argument


#tasks.add.delay(2,2)
#tasks.mul.delay(4,2)
#tasks.mul.delay(4,4)
#tasks.add.delay(4,4)

#q = RedisQueue('test')  
#q.put('Task 1')         
#q.put('Task 2')         
#q.put('Task 3')         
#q.put('Task 4')         

#result = tasks.basic_celery_task.delay()
print ("Started!")                         

flask_app.run(host="127.0.0.1",port=5001, threaded=True)    
