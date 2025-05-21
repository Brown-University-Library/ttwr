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
        Processes each incoming request:
        - If 'turnstile_verified' is in the session, the user has passed the challenge.
        - If the request path matches any exempt pattern, allow it.
        - Otherwise, render the Turnstile challenge template.
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

        ## allowed-ip-check -----------------------------------------
        ip: str = request.META.get('REMOTE_ADDR')
        log.debug(f'turnstile_middleware: ip, ``{ip}``')
        if TurnstileMiddlewareHelper.ip_is_valid(ip, settings.TURNSTILE_ALLOWED_IPS):
            log.debug('turnstile_middleware: ip is ok')
            return self.get_response(request)

        ## allowed-user-agent-check ---------------------------------
        # """ helper function isn't really needed, but facilitates tests """
        # user_agent: str = request.META.get('HTTP_USER_AGENT')
        # log.debug(f'turnstile_middleware: user_agent, ``{user_agent}``')
        # if TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, settings.TURNSTILE_ALLOWED_USER_AGENTS):
        #     log.debug('turnstile_middleware: user_agent is ok')
        #     return self.get_response(request)

        ## allowed-path-check ---------------------------------------
        # url_path: str = request.path
        # log.debug(f'turnstile_middleware: url_path, {url_path}')
        # if url_path in settings.TURNSTILE_ALLOWED_PATHS:
        #     log.debug('turnstile_middleware: url_path is ok')
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


class TurnstileMiddlewareHelper:
    """
    Helper class for Turnstile middleware.
    """

    @staticmethod
    def ip_is_valid(ip_str: str, allowed_ips: list[str]) -> bool:
        """
        Checks if the IP address is in the list of allowed IPs.
        Supports specific IP addresses, and CIDR notation, like '192.168.1.0/24'.

        Args:
            ip_str: The IP address to check.
            allowed_ips: List of allowed IPs. This'll be from settings, but passing in both facilitates testing.
        """
        ip_obj: ipaddress.IPv4Address = ipaddress.IPv4Address(ip_str)  # in case we need to do CIDR math
        for allowed_ip in allowed_ips:
            if '/' in allowed_ip:  # eg CIDR notation, like '192.168.1.0/24'
                network: ipaddress.IPv4Network = ipaddress.IPv4Network(allowed_ip)
                if ip_obj in network:
                    return True
            elif ip_str == allowed_ip:
                return True
        return False

    @staticmethod
    def user_agent_is_valid(user_agent_str: str, allowed_user_agents: list[str]) -> bool:
        """
        Checks if the user agent is in the list of allowed user agents.
        Not currently called, but ready to go if needed.

        Args:
            user_agent_str: The user agent to check.
            allowed_user_agents: List of allowed user agents.
        """
        for allowed_user_agent in allowed_user_agents:
            allowed_user_agent = allowed_user_agent.strip()
            user_agent_str = user_agent_str.strip()
            if user_agent_str == allowed_user_agent:
                return True
        return False
