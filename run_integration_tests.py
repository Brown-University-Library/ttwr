#!/usr/bin/env python
import sys
from os.path import abspath, dirname, join

import django
import dotenv
from django.conf import settings
from django.test.utils import get_runner

if __name__ == '__main__':
    SITE_ROOT = dirname(abspath(__file__))
    PROJECT_ROOT = dirname(SITE_ROOT)
    dotenv.read_dotenv(join(PROJECT_ROOT, '.env'))
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['integration_tests'])
    ## to just run one test:
    # failures = test_runner.run_tests(['integration_tests.tests.TestPrintsViews.test_specific_print'])
    sys.exit(bool(failures))
