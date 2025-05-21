"""
Middleware to enforce Cloudflare Turnstile verification via user session across the entire Django site.

This module defines a TurnstileMiddleware class that intercepts incoming HTTP requests and ensures users
have successfully completed the Turnstile challenge before accessing any protected pages.

It offers a few exemptions.
"""

import ipaddress
import logging
from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

log = logging.getLogger('rome')

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

        ## ip-check --------------------------------------------------
        ip: str = request.META.get('REMOTE_ADDR')
        log.debug(f'turnstile_middleware: ip, {ip}')
        if self.ip_is_valid(ip, settings.TURNSTILE_ALLOWED_IPS):
            log.debug('turnstile_middleware: ip is ok')
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
            'rome_templates/turnstile_challenge.html',
            context=context,
        )

    def ip_is_valid(self, ip_str: str, allowed_ips: list[str]) -> bool:
        """
        Checks if the IP address is in the list of allowed IPs.

        Args:
            ip_str: The IP address to check.
            allowed_ips: List of allowed IPs.
        """
        ip_obj: ipaddress.IPv4Address = ipaddress.IPv4Address(ip_str)
        for allowed_ip in allowed_ips:
            assert isinstance(allowed_ip, str)
            if '/' in allowed_ip:  # eg CIDR notation, like '192.168.1.0/24'
                network: ipaddress.IPv4Address = ipaddress.IPv4Address(allowed_ip, strict=False)
                if ip_obj in network:
                    return_val = True
            else:
                if ip_str == allowed_ip:
                    return_val = True
        log.debug(f'turnstile_middleware: return_val, ``{return_val}``')
        return return_val
