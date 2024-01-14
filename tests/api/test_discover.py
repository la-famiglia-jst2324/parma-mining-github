from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.github.api.dependencies.auth import authenticate
from parma_mining.github.api.main import app
from parma_mining.github.model import DiscoveryRequest, DiscoveryResponse
from parma_mining.mining_common.const import HTTP_200, HTTP_422
from parma_mining.mining_common.exceptions import ClientInvalidBodyError
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


@pytest.fixture
def mock_github_client(mocker) -> MagicMock:
    """Mocking GitHubClient's search_organizations method."""
    mock = mocker.patch(
        "parma_mining.github.api.main.GitHubClient.search_organizations"
    )
    mock.return_value = DiscoveryResponse(handles=["mock_handle"]).model_dump()
    return mock


# Test for successful discovery
def test_discover_endpoint_success(client: TestClient, mock_github_client: MagicMock):
    request_data = [
        DiscoveryRequest(company_id="123", name="TestCompany").model_dump(),
        DiscoveryRequest(company_id="456", name="AnotherCompany").model_dump(),
    ]

    response = client.post("/discover", json=request_data)
    assert response.status_code == HTTP_200
    assert isinstance(response.json(), dict)
    assert "identifiers" in response.json()
    assert "validity" in response.json()

    assert mock_github_client.called


def test_discover_endpoint_empty_request(client: TestClient):
    with pytest.raises(ClientInvalidBodyError) as exc_info:
        client.post("/discover", json=[])
    assert "Request body cannot be empty for discovery" in str(exc_info.value)


def test_discover_endpoint_invalid_format(client: TestClient):
    invalid_request_data = {"invalid": "data"}

    response = client.post("/discover", json=invalid_request_data)
    assert response.status_code == HTTP_422


def test_discover_non_existing_company(
    client: TestClient, mock_github_client: MagicMock
):
    mock_github_client.return_value = {}

    request_data = [
        DiscoveryRequest(company_id="999", name="NonExistingCompany").model_dump()
    ]
    response = client.post("/discover", json=request_data)

    assert response.status_code == HTTP_200
    response_data = response.json()
    assert response_data["identifiers"]["999"] == {"handles": []}


def test_discover_endpoint_with_github_client_error(
    client: TestClient, mock_github_client: MagicMock
):
    mock_github_client.side_effect = Exception("Mocked Exception")
    request_data = [DiscoveryRequest(company_id="123", name="TestCompany").model_dump()]

    with pytest.raises(Exception) as exc_info:
        client.post("/discover", json=request_data)
    assert "Mocked Exception" in str(exc_info.value)
