"""Main entrypoint for the API routes in of parma-analytics."""
from typing import List

from fastapi import FastAPI, HTTPException
from starlette import status

from parma_mining.github.client import GitHubClient
from parma_mining.github.model import (
    OrganizationModel,
    DiscoveryModel,
    CompaniesRequest,
)
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

github_token = os.getenv("GITHUB_TOKEN", "default-test-token")

github_client = GitHubClient(github_token)


# root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-github"}


@app.post(
    "/organizations",
    response_model=List[OrganizationModel],
    status_code=status.HTTP_200_OK,
)
def get_organization_details(companies: CompaniesRequest) -> List[OrganizationModel]:
    """Endpoint to get detailed information about a dict of organizations."""
    all_org_details = []
    for company_name, handles in companies.companies.items():
        for handle in handles:
            org_details = github_client.get_organization_details(handle)
            all_org_details.append(org_details)

    return all_org_details


@app.get(
    "/search/orgs",
    response_model=List[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def search_organizations(query: str):
    """Endpoint to search GitHub organizations based on a query."""
    return github_client.search_organizations(query)
