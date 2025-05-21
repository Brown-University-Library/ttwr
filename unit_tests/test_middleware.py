from config.middleware.turnstile_middleware import TurnstileMiddlewareHelper
from django.test import SimpleTestCase


class TestIPValidation(SimpleTestCase):
    def test_valid_ip_exact_match(self):
        """Test that exact IP matches are valid"""
        ip = '192.168.1.100'
        allowed_ips = ['192.168.1.100']
        self.assertTrue(TurnstileMiddlewareHelper.ip_is_valid(ip, allowed_ips))

    def test_invalid_ip_exact_match(self):
        """Test that non-matching exact IPs are invalid"""
        ip = '192.168.1.100'
        allowed_ips = ['192.168.1.101']
        self.assertFalse(TurnstileMiddlewareHelper.ip_is_valid(ip, allowed_ips))

    def test_valid_ip_cidr_match(self):
        """Test that IPs within CIDR range are valid"""
        ip = '192.168.1.100'
        allowed_ips = ['192.168.1.0/24']
        self.assertTrue(TurnstileMiddlewareHelper.ip_is_valid(ip, allowed_ips))

    def test_invalid_ip_cidr_match(self):
        """Test that IPs outside CIDR range are invalid"""
        ip = '192.168.2.100'
        allowed_ips = ['192.168.1.0/24']
        self.assertFalse(TurnstileMiddlewareHelper.ip_is_valid(ip, allowed_ips))

    def test_multiple_allowed_ips(self):
        """Test validation with multiple allowed IPs"""
        ip = '192.168.1.100'
        allowed_ips = ['192.168.1.100', '10.0.0.1', '192.168.1.0/24']
        self.assertTrue(TurnstileMiddlewareHelper.ip_is_valid(ip, allowed_ips))

    def test_invalid_ip_format(self):
        """Test that invalid IP format raises ValueError"""
        ip = 'not-an-ip'
        allowed_ips = ['192.168.1.100']
        with self.assertRaises(ValueError):
            TurnstileMiddlewareHelper.ip_is_valid(ip, allowed_ips)
