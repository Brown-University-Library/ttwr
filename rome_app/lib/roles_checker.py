"""
This script checks the Biography roles field for roles that are not in the Roles table.

Usage:
- cd ./ttwr
- export ROME__PROJECT_DIR_ROOT_PATH="/full/path/to/stuff/github_dir/"
- export ROME__DOTENV_PATH="/full/path/to/stuff/.env"
- source ../env/bin/activate
- python ./lib/roles_checker.py

Sample output:
Roles in Biography/Roles that are not in the Roles table:
{ 'name': 'Person_A', 'id': 1, 'invalid_roles: ['bad_role_A', 'bad_role_B'] }
{ 'name': 'Person_B', 'id': 2, 'invalid_roles: ['bad_role_C'] }
etc...
"""

import logging, os, pathlib, pprint, sys
import django, dotenv


## run code ---------------------------------------------------------
def run_code():
    """ Runs code.
        Called by `__main__`. """
    from rome_app.models import Biography, Role
    log.info( 'starting run_code()' )
    bios = Biography.objects.all()
    problems = []
    for (i, bio) in enumerate( bios ):
        roles = bio.roles
        log.info( f'roles, ``{roles}``' )
        split_roles = []
        if roles:
            split_roles = roles.split( ';' )
        log.info( f'split_roles, ``{split_roles}``' )
        validity = 'init'
        for role in split_roles:
            validity = check_role( role )
            log.debug( f'validity, ``{validity}``' )
        if i > 3:
            break
    log.info( 'end of run_code()' )
    return


def check_role( role_to_check: str ):
    """ Checks biography-role against Roles table.
        Called by `run_code()`. """
    from rome_app.models import Role
    log.info( f'role_to_check, ``{role_to_check}``' )
    try:
        role_lookup = Role.objects.get( text=role_to_check )
        validity_check = 'valid'
    except Exception as e:
        log.debug( f'exception, ``{e}``')
        log.exception( f'problem looking up role, ``' )
        validity_check = 'invalid'
    log.info( f'type(role_lookup), ``{type(role_lookup)}``' )    
    log.info( f'validity_check, ``{validity_check}``' )
    return validity_check


## helper -- setup logging ------------------------------------------
""" Called by `__main__`. """
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', 
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger( 'example_script' )
log.info( 'starting log' )


## helper -- setup environment --------------------------------------
def setup_environment():
    """ Updates sys.path and reads the .env settings.
        Called by `__main__`. """
    log.info( 'setting up environment' )
    ## allows bdr_tools to be imported ------------------------------
    PROJECT_ROOT = os.environ['ROME__PROJECT_DIR_ROOT_PATH']
    log.info( f'PROJECT_ROOT, ``{PROJECT_ROOT}``' )
    if PROJECT_ROOT not in sys.path:
        sys.path.append( PROJECT_ROOT )
    ## loads .env settings ------------------------------------------
    DOTENV_PATH = os.environ['ROME__DOTENV_PATH']
    log.info( f'DOTENV_PATH, ``{DOTENV_PATH}``' )
    try:
        dotenv.read_dotenv( DOTENV_PATH )
        log.info( 'dotenv successfully read' ) 
    except Exception as e:
        log.exception( 'problem reading dotenv' )
    ## loads django --------------------------------------------------
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    cwd = os.getcwd()   # assumes the cwd is the project directory
    if cwd not in sys.path:
        sys.path.append( cwd )
    django.setup()      # ok, now django-related imports will work
    log.info( 'django.setup() complete' )
    return


## caller -----------------------------------------------------------
if __name__ == "__main__":
    log.info( 'starting if __name__ == "__main__"')
    setup_environment()     # loads .env settings and envars
    run_code()              # THIS IS WHERE WORK IS DONE   
    log.info( 'eof' )


## eof
