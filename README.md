ttwr
====

This is the django app that runs the Theater That Was Rome project website.

#### Install and Run
- mkdir rome_project
- cd rome_project
- virtualenv -p /path/to/python2.7 env
- set environment variables in env/bin/activate and env/bin/activate_this.py
- git clone git@github.com:Brown-University-Library/ttwr.git (use https://github.com/Brown-University-Library/ttwr.git if you're not using SSH key)
- source env/bin/activate
- pip install --upgrade pip
- pip install -r ttwr/requirements.txt (requires compiler for compiling lxml)
- python manage.py migrate
- python manage.py collectstatic
- python manage.py runserver
