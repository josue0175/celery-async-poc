# celery-async-poc
run redis-server
celery -A proj worker --loglevel=info 
scl enable rh-python34 /bin/bash
python3.4 test.py
