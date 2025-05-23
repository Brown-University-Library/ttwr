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

    ## end class TestIPValidation


class TestUserAgentValidation(SimpleTestCase):
    """
    Tests for the TurnstileMiddlewareHelper.user_agent_is_valid() method.
    """

    def test_valid_user_agent_exact_match(self):
        """Test that exact user agent matches are valid"""
        user_agent = 'Mozilla/5.0'
        allowed_user_agents = ['Mozilla/5.0']
        self.assertTrue(TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, allowed_user_agents))

    def test_invalid_user_agent_exact_match(self):
        """Test that non-matching user agents are invalid"""
        user_agent = 'Mozilla/5.0'
        allowed_user_agents = ['Chrome/123']
        self.assertFalse(TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, allowed_user_agents))

    def test_empty_user_agent(self):
        """Test validation with empty user agent string"""
        user_agent = ''
        allowed_user_agents = ['']
        self.assertTrue(TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, allowed_user_agents))

    def test_multiple_allowed_user_agents(self):
        """Test validation with multiple allowed user agents"""
        user_agent = 'Mozilla/5.0'
        allowed_user_agents = ['Mozilla/5.0', 'Chrome/123', 'Safari/605']
        self.assertTrue(TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, allowed_user_agents))

    def test_no_allowed_user_agents(self):
        """Test validation with empty allowed user agents list"""
        user_agent = 'Mozilla/5.0'
        allowed_user_agents = []
        self.assertFalse(TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, allowed_user_agents))

    def test_whitespace_user_agent(self):
        """Test validation with whitespace user agent string"""
        user_agent = ' Mozilla/5.0 '
        allowed_user_agents = [' Mozilla/5.0 ']
        self.assertTrue(TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, allowed_user_agents))

    def test_case_sensitive_match(self):
        """Test that validation is case-sensitive"""
        user_agent = 'Mozilla/5.0'
        allowed_user_agents = ['mozilla/5.0']
        self.assertFalse(TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, allowed_user_agents))

    def test_special_characters(self):
        """Test validation with special characters in user agent"""
        user_agent = 'Mozilla/5.0 (iPhone)'
        allowed_user_agents = ['Mozilla/5.0 (iPhone)']
        self.assertTrue(TurnstileMiddlewareHelper.user_agent_is_valid(user_agent, allowed_user_agents))

    ## end class TestUserAgentValidation
