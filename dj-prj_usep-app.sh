#!/bin/sh

# NOTE: permissions updating requires root (suggestion: sudo bash ./this_script.sh)


# setup
APP_DIR_PATH='/opt/local/django_projects/projects/rome_app'
GIT_URL='https://bitbucket.org/ben_leveque/projects-rome_app.git'
MANAGE_PY_PATH='/opt/local/django_projects/projects/manage.py'
PYTHON_ENV_PATH='/opt/local/django_projects/projects/env/bin/python'
STATIC_WEB_DIR_PATH='/var/www/html/django_media/projects_media'
TOUCH_PATH='/opt/local/django_projects/projects/projects/apache/wsgi.py'

# update app
cd $APP_DIR_PATH
git pull $GIT_URL

# run collectstatic
$PYTHON_ENV_PATH $MANAGE_PY_PATH collectstatic --noinput

# cleanup media dir permssions
chmod -R u=rw,g=rw,o=r $STATIC_WEB_DIR_PATH  # recursively sets app file and directory permissions
chmod u=rwx,g=rwx,o=rx $STATIC_WEB_DIR_PATH  # properly sets the executable/searchable bit for the app directory
find $STATIC_WEB_DIR_PATH -type d | xargs chmod u=rwx,g=rwx,o=rx  # properly sets the executable/searchable bit for app sub-directories
chgrp -R javadev $STATIC_WEB_DIR_PATH  # recursively ensures all items are set to group javadev -- solves problem of an item being root/root if sudo-updated after a forced deletion

# cleanup app dir permissions
chmod -R u=rw,g=rw,o=r $APP_DIR_PATH  # recursively sets app file and directory permissions
chmod u=rwx,g=rwx,o=rx $APP_DIR_PATH  # properly sets the executable/searchable bit for the app directory
find $APP_DIR_PATH -type d | xargs chmod u=rwx,g=rwx,o=rx  # properly sets the executable/searchable bit for app sub-directories
chgrp -R javadev $APP_DIR_PATH  # recursively ensures all items are set to group javadev -- solves problem of an item being root/root if sudo-updated after a forced deletion

# make it real
touch $TOUCH_PATH

# [END]
