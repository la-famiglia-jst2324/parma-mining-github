from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.github.api.main import app
from parma_mining.mining_common.const import HTTP_200

client = TestClient(app)


@pytest.fixture
def mock_github_client(mocker) -> MagicMock:
    """Mocking GitHubClient's search_organizations method."""
    mock = mocker.patch(
        "parma_mining.github.api.main.GitHubClient.search_organizations"
    )
    mock.return_value = [{"name": "TestOrg", "url": "https://github.com/TestOrg"}]
    return mock


def test_search_organizations_success(mock_github_client: MagicMock):
    response = client.get("/search/companies?query=TestOrg")
    assert response.status_code == HTTP_200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "TestOrg"
    mock_github_client.assert_called_once()


"""
def test_search_organizations_empty_query():
    response = client.get("/search/companies?query=")
    assert response.status_code == HTTP_422
"""
