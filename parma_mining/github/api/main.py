"""Main entrypoint for the API routes in of parma-analytics."""
import json
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, status

from parma_mining.github.analytics_client import AnalyticsClient
from parma_mining.github.client import GitHubClient
from parma_mining.github.model import (
    CompaniesRequest,
    DiscoveryModel,
    ResponseModel,
)
from parma_mining.github.normalization_map import GithubNormalizationMap

env = os.getenv("env", "local")

if env == "prod":
    logging.basicConfig(level=logging.INFO)
elif env in ["staging", "local"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warning(f"Unknown environment '{env}'. Defaulting to INFO level.")
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

github_token = str(os.getenv("GITHUB_TOKEN", "default-test-token"))

github_client = GitHubClient(github_token)
analytics_client = AnalyticsClient()
normalization = GithubNormalizationMap()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-github"}


@app.get("/initialize", status_code=status.HTTP_200_OK)
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
    status_code=status.HTTP_200_OK,
)
def get_organization_details(companies: CompaniesRequest):
    """Endpoint to get detailed information about a dict of organizations."""
    for company_id, company_data in companies.companies.items():
        for data_type, handles in company_data.items():
            for handle in handles:
                if data_type == "name":
                    org_details = github_client.get_organization_details(handle)
                    data = ResponseModel(
                        source_name="github",
                        company_id=company_id,
                        raw_data=org_details,
                    )
                    # Write data to db via endpoint in analytics backend
                    try:
                        analytics_client.feed_raw_data(data)
                    except Exception as e:
                        logger.error(
                            f"Can't send crawling data to the Analytics. Error: {e}"
                        )
                else:
                    logger.error(f"Unsupported type error for {data_type} in {handle}")
    return "done"


@app.get(
    "/search/companies",
    response_model=list[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def search_organizations(query: str):
    """Endpoint to search GitHub organizations based on a query."""
    return github_client.search_organizations(query)
