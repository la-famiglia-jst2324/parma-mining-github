"""Main entrypoint for the API routes in of parma-analytics."""
from typing import List

from fastapi import FastAPI
from starlette import status

from parma_mining.github.client import GitHubClient
from parma_mining.github.model import OrganizationModel
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Access GitHub token from env
github_token = os.getenv("GITHUB_TOKEN")

app = FastAPI()

# Initialize GitHubClient
token = github_token
github_client = GitHubClient(token)


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
def get_organization_details(org_name: str):
    """Endpoint to get detailed information about a given organization."""
    org_details = github_client.get_organization_details(org_name)
    return org_details
