# dstp

- sudo apt install python3-pip

- sudo apt install python3-venv

- sudo python3 -m venv my_env

- start venv : source my_env/bin/activate
- close venv : deactivate

- install django : pip install django

# Server for IOT data

# command

- create new virtual environment
  - python -m venv env
- activate/deactivate environment
  - env\Scripts\Activate.ps1
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

- pip install pymongo==3.12.3
- pip install djongo

- python manage.py makemigrations
- python manage.py migrate
