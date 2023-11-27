"""Main entrypoint for the API routes in of parma-analytics."""
from fastapi import FastAPI
from starlette import status

from parma_mining.github.client import GitHubClient
from parma_mining.github.model import OrganizationModel
from dotenv import load_dotenv
import os

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

app = FastAPI()

token = os.getenv("GITHUB_TOKEN")

if github_token is None:
    raise ValueError("GITHUB_TOKEN environment variable must be set")
else:
    github_client = GitHubClient(github_token)


# root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-github"}


# Endpoint to retrieve Github information about an organization
@app.get(
    "/organization/{org_name}",
    response_model=OrganizationModel,
    status_code=status.HTTP_200_OK,
)
def get_organization_details(org_name: str) -> OrganizationModel:
    """Endpoint to get detailed information about a given organization."""
    org_details = github_client.get_organization_details(org_name)
    return org_details
