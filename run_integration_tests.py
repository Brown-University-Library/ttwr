#!/usr/bin/env python
from os.path import dirname, abspath, join
import sys 
import dotenv
import django
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
    sys.exit(bool(failures))
