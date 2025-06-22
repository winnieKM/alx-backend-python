#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
import sys
import os

# Allow imports from parent directory (for client.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns the correct JSON payload."""
        client = GithubOrgClient(org_name)
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Access property, which should call get_json once
        org_data = client.org
        self.assertEqual(org_data, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test _public_repos_url returns repos_url from org property."""
        client = GithubOrgClient("test_org")

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked_url.com/repos"}

            self.assertEqual(client._public_repos_url, "http://mocked_url.com/repos")
            mock_org.assert_called_once()

    @patch('client.GithubOrgClient.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repo names."""
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_repos

        client = GithubOrgClient("test_org")

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://mocked_url.com/repos"

            repos = client.public_repos()
            self.assertEqual(repos, test_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://mocked_url.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean based on license key."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
