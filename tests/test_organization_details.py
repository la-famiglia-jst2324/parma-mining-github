import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from starlette import status
from unittest.mock import MagicMock
from parma_mining.github.api.main import app

client = TestClient(app)


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
                "stargazers_count": 10,
                "watchers_count": 5,
                "forks_count": 3,
                "open_issues_count": 2,
                "stars": 10,
                "forks": 3,
            }
        ],
    }
    return mock


def test_get_organization_details(mock_github_client: MagicMock):
    payload = {
        "companies": {
            "Example_id1": {"name": ["langfuse"]},
            "Example_id2": {"name": ["personio"]},
        }
    }

    response = client.post("/companies", json=payload)

    assert response.status_code == 200

    assert response.json() == [
        {
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
                    "stargazers_count": 10,
                    "watchers_count": 5,
                    "forks_count": 3,
                    "open_issues_count": 2,
                    "stars": 10,
                    "forks": 3,
                }
            ],
        },
        {
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
                    "stargazers_count": 10,
                    "watchers_count": 5,
                    "forks_count": 3,
                    "open_issues_count": 2,
                    "stars": 10,
                    "forks": 3,
                }
            ],
        },
    ]


def test_get_organization_details_bad_request(mocker):
    mocker.patch(
        "parma_mining.github.api.main.GitHubClient.get_organization_details",
        side_effect=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        ),
    )

    payload = {
        "companies": {
            "Example_id1": {"name": ["langfuse"]},
            "Example_id2": {"name": ["personio"]},
        }
    }

    response = client.post("/companies", json=payload)
    assert response.status_code == 404
