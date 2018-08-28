from __future__ import absolute_import, unicode_literals
from celery import Celery

#import time,datetime
#import sys,os
#from celery import current_app
#from celery.bin import worker
#import celery.bin.base
#import celery.bin.celery
#import celery.platforms
#
#current_app.conf.CELERY_ALWAYS_EAGER = True
#current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
#
#from celery.utils import LOG_LEVELS
#current_app.conf.CELERYD_LOG_LEVEL = LOG_LEVELS['DEBUG']  # pretty much the same as logging.DEBUG


#app = Flask(__name__)
#app.config.from_object('config')
app = Celery('proj',
             broker='redis://localhost:6379',
             backend='redis://localhost:6379',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

#def make_celery(app):
#    # create context tasks in celery
#    celery = Celery(
#        app.import_name,
#        broker=app.config['BROKER_URL']
#    )
#    celery.conf.update(app.config)
#    celery.config_from_object(celeryconfig)
#    TaskBase = celery.Task
#
#    class ContextTask(TaskBase):
#        abstract = True
#
#        def __call__(self, *args, **kwargs):
#            with app.app_context():
#                return TaskBase.__call__(self, *args, **kwargs)
#
#    celery.Task = ContextTask
#
#    return celery

#celery = make_celery(app)


#@app.route('/')
#def view():
#    return "Hello, Flask is up and running!"


if __name__ == "__main__":
    app.start()
#    worker = worker.worker(app=app)
#    options = {
#        'broker': 'redis://localhost:6379',
#        'loglevel': 'INFO',
#        'logfile':'/var/log/rackmanager/celery.log',
#        'traceback': True,
#    }

#
##    worker.run(**options)
#
#    app.run()
#

