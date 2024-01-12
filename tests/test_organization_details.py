import logging
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from parma_mining.github.api.dependencies.auth import authenticate
from parma_mining.github.api.main import app
from parma_mining.mining_common.const import HTTP_200, HTTP_404
from tests.dependencies.mock_auth import mock_authenticate


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


logger = logging.getLogger(__name__)


@pytest.fixture
def mock_github_client(mocker) -> MagicMock:
    """Mocking the GitHubClient's method to avoid actual API calls during testing."""
    mock = mocker.patch(
        "parma_mining.github.api.main.GitHubClient.get_organization_details"
    )
    mock.return_value = {
        "name": "TestOrg",
        "description": "A test organization",
        "url": "https://github.com/TestOrg",
        "repos": [
            {
                "name": "TestRepo",
                "description": "A test repository",
                "language": "Python",
                "created_at": "2021-01-01T00:00:00Z",
                "updated_at": "2021-01-02T00:00:00Z",
                "pushed_at": "2021-01-03T00:00:00Z",
                "html_url": "https://github.com/TestOrg/TestRepo",
                "clone_url": "https://github.com/TestOrg/TestRepo.git",
                "svn_url": "https://svn.github.com/TestOrg/TestRepo",
                "homepage": "https://testrepo.com",
                "size": 100,
                "watchers_count": 5,
                "open_issues_count": 2,
                "stars": 10,
                "forks": 3,
            }
        ],
        "aggregated_sum_size": 100,
        "aggregated_sum_watchers_count": 5,
        "aggregated_sum_open_issues_count": 2,
        "aggregated_sum_stars": 10,
        "aggregated_sum_forks": 3,
    }
    return mock


@pytest.fixture
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.github.api.main.AnalyticsClient.feed_raw_data")
    mock = mocker.patch(
        "parma_mining.github.api.main.AnalyticsClient.crawling_finished"
    )
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock


def test_get_organization_details(
    mock_github_client: MagicMock, mock_analytics_client: MagicMock, client: TestClient
):
    payload = {
        "task_id": 123,
        "companies": {
            "Example_id1": {"name": ["langfuse"]},
            "Example_id2": {"name": ["personio"]},
        },
    }

    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)

    mock_analytics_client.assert_called()

    assert response.status_code == HTTP_200


def test_get_organization_details_bad_request(mocker, client: TestClient):
    mocker.patch(
        "parma_mining.github.api.main.GitHubClient.get_organization_details",
        side_effect=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        ),
    )

    payload = {
        "task_id": 123,
        "companies": {
            "Example_id1": {"name": ["langfuse"]},
            "Example_id2": {"name": ["personio"]},
        },
    }

    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)
    assert response.status_code == HTTP_404
