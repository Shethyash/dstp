# dstp

# dependencies

- sudo apt install python3-pip
- sudo apt install python3-venv
- sudo python3 -m venv my_env
- pip install django
- pip install django-crontab
- pip install pymongo==3.12.3
- pip install djongo

# command

- create new virtual environment
  - python -m venv env
- activate/deactivate environment
  - env\Scripts\Activate.ps1
  - source my_env/bin/activate
  - deactivate
- install django
  - pip install django
- txt file for version
  - python -m pip freeze > requirements.txt
- install all dependency
  - python -m pip install -r requirements.txt
- create new django project
  - django-admin startproject name
- start project
  - python manage.py startapp name
- run django server
  - python manage.py runserver
- create new model
  - python manage.py startapp name

# mongo db

https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

- python manage.py makemigrations
- python manage.py migrate
- start mongo server : sudo systemctl start mongod
- mongo
- use iot_db

# cron Job

https://gutsytechster.wordpress.com/2019/06/24/how-to-setup-a-cron-job-in-django/

- add cron jobs : python manage.py crontab add
- active cron job list : python manage.py crontab show
- remove cron job : python manage.py crontab remove
