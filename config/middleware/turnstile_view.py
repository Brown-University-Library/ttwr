"""
Turnstile verification view. 
Learn more about Turnstile at: https://developers.cloudflare.com/turnstile/

View called from ttwr/config/urls.py
"""

import logging
from typing import Any, Optional

import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

log = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def turnstile_verify(request: HttpRequest) -> HttpResponse:
    log.info('starting turnstile_verify()')

    token: Optional[str] = request.POST.get('token')
    if not token:
        log.error('missing token in request, unable to verify')
        return HttpResponseForbidden('missing turnstile token')

    # — verify with Cloudflare
    log.debug('verifying token with Cloudflare')
    resp: requests.Response = requests.post(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        data={
            'secret': settings.TURNSTILE_SECRET_KEY,
            'response': token,
            'remoteip': request.META.get('REMOTE_ADDR'),
        },
        timeout=5,
    )
    result: dict[str, Any] = resp.json()

    if result.get('success'):
        request.session['turnstile_verified'] = True
        log.debug('turnstile verification successful')
        return JsonResponse({'ok': True})
    else:
        error_codes = result.get('error-codes')
        log.error(f'turnstile verification failed: {error_codes}')
        return JsonResponse({'ok': False, 'reason': error_codes}, status=403)
