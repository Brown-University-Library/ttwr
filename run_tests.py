#!/usr/bin/env python
import os
import sys 
import tempfile


if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.unit_tests'
    os.environ['ROME_BDR_SERVER'] ='localhost'
    os.environ['ROME_PID_PREFIX'] ='testsuite'
    os.environ['ROME_BDR_IDENTITY'] ='ID1'
    os.environ['ROME_BDR_AUTH_CODE'] = '12345'
    os.environ['ROME_BDR_AUTH_CODE'] = '12345'
    with tempfile.TemporaryDirectory() as tmp:
        os.environ['LOG_DIR'] = tmp
        django.setup()
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        failures = test_runner.run_tests(['unit_tests'])
    sys.exit(bool(failures))
