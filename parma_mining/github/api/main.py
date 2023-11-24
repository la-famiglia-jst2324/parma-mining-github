"""Main entrypoint for the API routes in of parma-analytics."""
from typing import List

from fastapi import FastAPI
from parma_mining.github.client import GitHubClient
from parma_mining.github.model import OrganizationModel
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env

# Now you can access your GitHub token like this
github_token = os.getenv("GITHUB_TOKEN")

app = FastAPI()

# Initialize GitHubClient with your token
token = github_token  # Replace with your actual GitHub access token
github_client = GitHubClient(token)


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-github"}


# Endpoint to retrieve Github information about an organization
@app.get("/{org_name}", response_model=OrganizationModel)
def get_organization_details(org_name: str):
    """Endpoint to get detailed information about a given organization."""
    org_details = github_client.get_organization_details(org_name)
    return org_details
