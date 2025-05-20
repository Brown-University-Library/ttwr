"""
Middleware to enforce Cloudflare Turnstile verification via user session across the entire Django site.

This module defines a TurnstileMiddleware class that intercepts incoming HTTP requests and ensures users
have successfully completed the Turnstile challenge before accessing any protected pages. It checks for a
session flag named "turnstile_verified" (set upon successful verification) or allows requests to certain
exempt paths (e.g., the turnstile-verify endpoint and static assets). All other requests render a lightweight
challenge page that, upon success, should set the session flag in the view.
"""

import logging
from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

log = logging.getLogger(__name__)

log.debug('turnstile_middleware: loaded')
log.debug(f'turnstile_middleware: turnstile-verify url, `{reverse("turnstile-verify")}`')


class TurnstileMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """
        Initialize the middleware.

        Args:
            get_response: The next middleware or the view callable.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process each incoming request:
        1. If 'turnstile_verified' is in the session, the user has passed the challenge.
        2. If the request path matches any exempt pattern, allow it.
        3. Otherwise, render the Turnstile challenge template.
        """
        log.debug('turnstile_middleware: starting __call__()')
        log.debug(f'turnstile_middleware: request path, {request.path}')

        ## session-check -------------------------------------------
        if request.session.get('turnstile_verified'):
            log.debug('turnstile_middleware: already verified via session')
            return self.get_response(request)

        ## verify-url-check ------------------------------------------
        if 'turnstile-verify' in request.path:
            log.debug('turnstile_middleware: exempt path, turnstile-verify')
            return self.get_response(request)

        ## exempt-path-check -----------------------------------------
        # if any(pattern.match(request.path) for pattern in settings.TURNSTILE_EXEMPT_PATHS):
        #     log.debug('turnstile_middleware: exempt path from settings')
        #     return self.get_response(request)

        ## show-challenge ------------------------------------------
        log.debug('turnstile_middleware: rendering challenge')
        verify_url = request.build_absolute_uri(reverse('turnstile-verify'))
        log.debug(f'turnstile_middleware: verify_url, {verify_url}')
        context = {
            'site_key': settings.TURNSTILE_SITE_KEY,
            'verify_url': verify_url,
            'turnstile_email': settings.TURNSTILE_EMAIL,
        }
        return render(
            request,
            'turnstile_challenge.html',
            context=context,
        )
