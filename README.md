# Tasker

Tasker App

1)First, you might need to install virtualenv, which you can get with pip:

Type this command on the terminal: 
(sudo) pip install virtualenv

2)Copy the tasker_app folder to your workspace

3)From your workspace, you can then create a virtualenv with Python 3.4 (use which python3 to find path)

Type this command on the terminal:
virtualenv -p {path to python 3} tasker_app

4)Install project python package dependencies with pip
first, activate the virtualenv

source bin/activate 
pip install --upgrade -r etc/pip/tasker.packages

5)Open the src folder and test the project using runserver 
You should now be able to test everything is working with runserver.

run migrations
python manage.py migrate

run server
python manage.py runserver

Test the application
python manage.py test
