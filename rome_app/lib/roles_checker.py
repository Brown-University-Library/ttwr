"""
This script checks the Biography roles field for roles that are not in the Roles table.

Usage:
- cd ./ttwr
- export ROME__PROJECT_DIR_ROOT_PATH="/full/path/to/stuff/github_dir/"
- export ROME__DOTENV_PATH="/full/path/to/stuff/.env"
- export ROME__LOG_LEVEL="DEBUG"
- source ../env/bin/activate
- python ./lib/roles_checker.py

Sample output:
Roles in Biography/Roles that are not in the Roles table:
{ 'name': 'Person_A', 'id': 1, 'invalid_roles': ['bad_role_A', 'bad_role_B'] }
{ 'name': 'Person_B', 'id': 2, 'invalid_roles': ['bad_role_C'] }
etc...
"""

import json, logging, os, pathlib, pprint, sys
import django, dotenv

""" Allows script to be run from command-line or as import. """
try:
    level_dict = { 'DEBUG': logging.DEBUG, 'INFO': logging.INFO }
    ENVAR_LOG_LEVEL = os.environ['ROME__LOG_LEVEL']
    print( f'ENVAR_LOG_LEVEL, ``{ENVAR_LOG_LEVEL}``' )
    LEVEL_OBJECT = level_dict[ ENVAR_LOG_LEVEL ]
    logging.basicConfig(
        level=LEVEL_OBJECT,
        format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', 
        datefmt='%d/%b/%Y %H:%M:%S' )
    log = logging.getLogger( 'example_script' )
    log.debug( 'starting log' )
except Exception as e:
    log = logging.getLogger(__name__)


## run code ---------------------------------------------------------
def run_code():
    """ Runs code.
        Called by `__main__`. """
    from rome_app.models import Biography, Role
    log.debug( 'starting run_code()' )
    bios = Biography.objects.all().order_by( 'name' )
    problems = []
    for (i, bio) in enumerate( bios ):
        error_entry = { 'name': bio.name, 'id': bio.id, 'invalid_roles': [] }  # type: ignore -- `id` is valid.
        log.debug( f'checking bio.name, ``{bio.name}``' )
        roles = bio.roles
        log.debug( f'roles, ``{roles}``' )
        split_roles = []
        if roles:
            split_roles = roles.split( ';' )
        log.debug( f'split_roles, ``{split_roles}``' )
        validity = 'init'
        for role in split_roles:
            role = role.strip()
            validity = check_role( role )
            if validity == 'invalid':
                error_entry['invalid_roles'].append( role )
        if error_entry['invalid_roles']:
            problems.append( error_entry )
        # if i > 10:
        #     break
    log.info( f'problems, ``{pprint.pformat(problems, sort_dicts=False)}``' )
    # jsn = json.dumps( problems, sort_keys=False, indent=2 )
    # log.info( f'jsn, ``{jsn}``')
    # log.info( f'number of problem-entries, ``{len(problems)}``' )
    # log.debug( 'end of run_code()' )
    # return jsn
    log.info( f'number of problem-entries, ``{len(problems)}``' )
    log.debug( 'end of run_code()' )
    return problems


def check_role( role_to_check: str ):
    """ Checks biography-role against Roles table.
        Called by `run_code()`. """
    from rome_app.models import Role
    log.debug( f'role_to_check (stripped), ``{role_to_check}``' )
    try:
        role_lookup = Role.objects.get( text__exact=role_to_check )
        log.debug( f'type(role_lookup), ``{type(role_lookup)}``' )
        validity_check = 'valid'
    except Exception as e:
        log.debug( f'exception, ``{e}``')
        log.debug( f'role, ``{role_to_check}`` not found' )
        validity_check = 'invalid'
    log.debug( f'validity_check, ``{validity_check}``' )
    return validity_check




## helper -- setup environment --------------------------------------
def setup_environment():
    """ Updates sys.path and reads the .env settings.
        Called by `__main__`. """
    log.debug( 'setting up environment' )
    ## allows bdr_tools to be imported ------------------------------
    PROJECT_ROOT = os.environ['ROME__PROJECT_DIR_ROOT_PATH']
    log.debug( f'PROJECT_ROOT, ``{PROJECT_ROOT}``' )
    if PROJECT_ROOT not in sys.path:
        sys.path.append( PROJECT_ROOT )
    ## loads .env settings ------------------------------------------
    DOTENV_PATH = os.environ['ROME__DOTENV_PATH']
    log.debug( f'DOTENV_PATH, ``{DOTENV_PATH}``' )
    try:
        dotenv.read_dotenv( DOTENV_PATH )
        log.debug( 'dotenv successfully read' ) 
    except Exception as e:
        log.exception( 'problem reading dotenv' )
    ## loads django --------------------------------------------------
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    cwd = os.getcwd()   # assumes the cwd is the project directory
    if cwd not in sys.path:
        sys.path.append( cwd )
    django.setup()      # ok, now django-related imports will work
    log.debug( 'django.setup() complete' )
    return


## caller -----------------------------------------------------------
if __name__ == "__main__":
    log.debug( 'starting if __name__ == "__main__"')
    setup_environment()     # loads .env settings and envars
    run_code()              # THIS IS WHERE WORK IS DONE   
    log.debug( 'eof' )


## eof
