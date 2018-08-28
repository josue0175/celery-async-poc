from proj import tasks
from flask import Flask
from flask import request, Response, jsonify, url_for
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
    tcall=tasks.celpost.apply_async(args=['http://localhost:5001/tests/endpoint',rdata],countdown=2)
    task=tasks.celpost.AsyncResult(tcall.id)
    print("state %s" % task.state)
#    if task.state == 'PENDING':
#        # job did not start yet
#        response = {
#            'state': task.state,
#            'current': 0,
#            'total': 1,
#            'status': 'Pending...'
#        }
#    elif task.state != 'FAILURE':
#        response = {
#            'state': task.state,
#            'current': task.info.get('current', 0),
#            'total': task.info.get('total', 1),
#            'status': task.info.get('status', '')
#        }
#        if 'result' in task.info:
#            response['result'] = task.info['result']
#    else:
#        # something went wrong in the background job
#        response = {
#            'state': task.state,
#            'current': 1,
#            'total': 1,
#            'status': str(task.info),  # this is the exception raised
#        }
    #print("sendEvents: response from server %s" % res)
    #print("sendEvents: json response %s" % res.json())

    print("taskid %s" % tcall.id)

    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=tcall.id)}

#WORKING BELOW
#    r=None
#    while not r=='SUCCESS':
#        r=task.state
#        print("state %s" % r)
#        print("task %s" % task.info)
#        time.sleep(0.4)
#
#    print("sendEvents: state %s" % task.state)
#    print("sendEvents: response %s" % task.info)
#    return "Got response"


@flask_app.route('/status/<task_id>')
def taskstatus(task_id):
    task=tasks.celpost.AsyncResult(task_id)
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
            'current': task.info['current'],
            'total': task.info['total'],
            #'status': task.info.get('status', '')
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
    return jsonify(response)

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
