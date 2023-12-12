"""Main entrypoint for the API routes in of parma-analytics."""
import json
from typing import List
from fastapi import FastAPI
from starlette import status
from parma_mining.github.analytics_client import AnalyticsClient
from parma_mining.github.client import GitHubClient
from parma_mining.github.model import (
    OrganizationModel,
    DiscoveryModel,
    CompaniesRequest,
)
from dotenv import load_dotenv
import os

from parma_mining.github.normalization_map import GithubNormalizationMap

load_dotenv()

app = FastAPI()

github_token = os.getenv("GITHUB_TOKEN", "default-test-token")

github_client = GitHubClient(github_token)
analytics_client = AnalyticsClient()
normalization = GithubNormalizationMap()


# root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-github"}


# initialization endpoint
@app.get("/initialize", status_code=200)
def initialize(source_id: int) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "weekly"
    normalization_map = GithubNormalizationMap().get_normalization_map()
    # register the measurements to analytics
    analytics_client.register_measurements(
        normalization_map, source_module_id=source_id
    )

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


@app.post(
    "/companies",
    response_model=List[OrganizationModel],
    status_code=status.HTTP_200_OK,
)
def get_organization_details(companies: CompaniesRequest) -> List[OrganizationModel]:
    """Endpoint to get detailed information about a dict of organizations."""
    all_org_details = []
    for company_id, company_data in companies.companies.items():
        for data_type, handles in company_data.items():
            for handle in handles:
                if data_type == "name":
                    org_details = github_client.get_organization_details(handle)
                    all_org_details.append(org_details)
                else:
                    # To be included in logging
                    print("Unsupported type error")
    return all_org_details


@app.get(
    "/search/companies",
    response_model=List[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def search_organizations(query: str):
    """Endpoint to search GitHub organizations based on a query."""
    return github_client.search_organizations(query)
