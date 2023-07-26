import datetime, json, logging, os, pprint, subprocess

import trio
from django.conf import settings

log = logging.getLogger(__name__)


def make_context( request, rq_now, info_txt ):
    """ Assembles data-dct.
        Called by views.version() """
    context = {
        'request': {
        'url': '%s://%s%s' % (
            request.scheme,
            request.META.get( 'HTTP_HOST', '127.0.0.1' ),  # HTTP_HOST doesn't exist for client-tests
            request.META.get('REQUEST_URI', request.META['PATH_INFO'])
            ),
        'timestamp': str( rq_now )
        },
        'response': {
            'ip': request.META.get('REMOTE_ADDR', 'unknown'),
            'version': info_txt,
            'timetaken': str( datetime.datetime.now() - rq_now )
        }
    }
    return context


class GatherCommitAndBranchData:

    def __init__( self ):
        self.commit_data = ''
        self.branch_data = ''
        # self.results_dct = {}

    async def manage_git_calls( self ):
        """ Triggers calling subprocess commands concurrently.
            Called by views.version() """
        log.debug( 'manage_git_calls' )
        results_holder_dct = {}  # receives git responses as they're produced
        async with trio.open_nursery() as nursery:
            nursery.start_soon( self.fetch_commit_data, results_holder_dct )
            nursery.start_soon( self.fetch_branch_data, results_holder_dct )  
        log.debug( f'final results_holder_dct, ```{pprint.pformat(results_holder_dct)}```' )
        self.commit = results_holder_dct['commit']
        self.branch = results_holder_dct['branch']
        return

    async def fetch_commit_data( self, results_holder_dct ):
        """ Fetches commit-data.
            Called by manage_git_calls() """
        log.debug( 'fetch_commit_data' )
        original_directory = os.getcwd()
        git_dir = settings.BASE_DIR
        os.chdir( git_dir )
        output_obj: subprocess.CompletedProcess = await trio.run_process( ['git', 'log'], capture_stdout=True )
        output: str = output_obj.stdout.decode( 'utf-8' )
        os.chdir( original_directory )
        lines = output.split( '\n' )
        commit = lines[0]
        results_holder_dct['commit'] = commit
        return

    async def fetch_branch_data( self, results_holder_dct ):
        """ Fetches branch-data.
            Called by manage_git_calls() """
        log.debug( 'fetch_branch_data' )
        original_directory = os.getcwd()
        git_dir = settings.BASE_DIR
        os.chdir( git_dir )
        output_obj: subprocess.CompletedProcess = await trio.run_process( ['git', 'branch'], capture_stdout=True )
        output: str = output_obj.stdout.decode( 'utf-8' )
        os.chdir( original_directory )
        lines = output.split( '\n' )
        branch = 'init'
        for line in lines:
            if line[0:1] == '*':
                branch = line[2:]
                break
        results_holder_dct['branch'] = branch
        return

## end class GatherCommitAndBranchData
