#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py
"""

import unittest
from unittest.mock import patch, Mock
import sys
import os

# Allow imports from parent directory (for client.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test _public_repos_url property returns correct URL based on org property."""
        client = GithubOrgClient("testorg")

        # Patch the 'org' property to return a dict with repos_url
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
            expected_url = "https://api.github.com/orgs/testorg/repos"
            self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.GithubOrgClient.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repos."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        client = GithubOrgClient("testorg")
        repos = client.public_repos()

        self.assertEqual(repos, [{"name": "repo1"}, {"name": "repo2"}])
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")

    def test_has_license(self):
        """Test has_license returns True only for matching license."""
        client = GithubOrgClient("testorg")

        repo_mit = {"license": {"key": "mit"}}
        repo_apache = {"license": {"key": "apache-2.0"}}
        repo_none = {}

        self.assertTrue(client.has_license(repo_mit, "mit"))
        self.assertFalse(client.has_license(repo_apache, "mit"))
        self.assertFalse(client.has_license(repo_none, "mit"))


if __name__ == "__main__":
    unittest.main()
