"""Main entrypoint for the API routes in of parma-analytics."""
from fastapi import FastAPI, HTTPException
from starlette import status

from parma_mining.github.client import GitHubClient
from parma_mining.github.model import OrganizationModel
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


@app.get(
    "/organization/{org_name}",
    response_model=OrganizationModel,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Organization not found"}},
)
def get_organization_details(org_name: str) -> OrganizationModel:
    """Endpoint to get detailed information about a given organization."""
    org_details = github_client.get_organization_details(org_name)
    return org_details
