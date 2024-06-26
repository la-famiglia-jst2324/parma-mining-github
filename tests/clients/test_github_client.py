from unittest.mock import MagicMock, patch

import pytest

from parma_mining.github.client import GitHubClient
from parma_mining.github.model import DiscoveryResponse, OrganizationModel
from parma_mining.mining_common.exceptions import ClientError, CrawlingError


@pytest.fixture
def github_client():
    return GitHubClient("dummy_token")


@patch("github.Github.get_organization")
def test_get_organization_details_success(mock_get_org, github_client):
    mock_org = MagicMock()
    mock_org.name = "TestOrg"
    mock_org.description = "Test Description"
    mock_org.html_url = "http://testorg.com"
    mock_org.get_repos.return_value = []
    mock_get_org.return_value = mock_org

    org_details = github_client.get_organization_details("TestOrg")
    assert org_details.name == "TestOrg"
    assert org_details.description == "Test Description"
    assert org_details.url == "http://testorg.com"
    assert isinstance(org_details, OrganizationModel)


@patch("github.Github.get_organization")
def test_get_organization_details_exception(mock_get_org, github_client):
    exception_instance = CrawlingError("Error fetching organization details!")
    mock_get_org.side_effect = exception_instance
    with pytest.raises(CrawlingError):
        github_client.get_organization_details("TestOrg")


@patch("github.Github.search_users")
def test_search_organizations_success(mock_search_users, github_client):
    mock_org = MagicMock()
    mock_org.login = "TestOrg"
    mock_org.html_url = "http://testorg.com"
    mock_search_users.return_value = [mock_org]

    results = github_client.search_organizations("Test")
    assert isinstance(results, DiscoveryResponse)
    assert len(results.handles) == 1
    assert results.handles[0] == "TestOrg"


@patch("github.Github.search_users")
def test_search_organizations_exception(mock_search_users, github_client):
    mock_search_users.side_effect = ClientError()
    with pytest.raises(ClientError):
        github_client.search_organizations("Test")
