"""
Turnstile verification view.
Learn more about Turnstile at: https://developers.cloudflare.com/turnstile/

View called from ttwr/config/urls.py
"""

import logging
import pprint
from typing import Any, Optional

import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

log = logging.getLogger('rome')


@csrf_exempt
@require_POST
def turnstile_verify(request: HttpRequest) -> HttpResponse:
    log.info('starting turnstile_verify()')

    ## get-token ----------------------------------------------------
    token: Optional[str] = request.POST.get('token')
    if not token:
        log.error('missing token in request, unable to verify')
        return HttpResponseForbidden('missing turnstile token')

    ## verify against Cloudflare ------------------------------------
    log.debug('verifying token with Cloudflare')
    data = {
        'secret': settings.TURNSTILE_SECRET_KEY,
        'response': token,
        'remoteip': request.META.get('REMOTE_ADDR'),
    }
    log.debug(f'data for turnstile verification, ``{pprint.pformat(data)}``')
    try:
        resp: requests.Response = requests.post(
            settings.TURNSTILE_API_URL,
            data=data,
            timeout=settings.TURNSTILE_API_TIMEOUT,
        )
        result: dict[str, Any] = resp.json()
        log.debug(f'turnstile verification result, ``{pprint.pformat(result)}``')
    except Exception:
        log.exception('turnstile verification failed')
        log.debug(f'turnstile-api-url, ``{settings.TURNSTILE_API_URL}``')
        log.debug(f'turnstile-timeout, ``{settings.TURNSTILE_API_TIMEOUT}``')
        return JsonResponse({'ok': False, 'reason': 'timeout'}, status=403)

    ## handle result ------------------------------------------------
    if result.get('success'):
        request.session['turnstile_verified'] = True
        ## set session expiry ---------------------------------------
        request.session.set_expiry(settings.TURNSTILE_SESSION_EXPIRY_MINUTES * 60)
        log.debug('turnstile verification successful')
        return JsonResponse({'ok': True})
    else:
        error_codes = result.get('error-codes')
        log.error(f'turnstile verification failed: {error_codes}')
        return JsonResponse({'ok': False, 'reason': error_codes}, status=403)
