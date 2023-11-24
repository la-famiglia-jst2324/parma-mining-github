"""Main entrypoint for the API routes in of parma-analytics."""
from typing import List

from fastapi import FastAPI

from parma_mining.github.client import GitHubClient

app = FastAPI()

# Initialize GitHubClient with your token
token = "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"  # Replace with your actual GitHub access token
github_client = GitHubClient(token)


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-github"}


@app.get("/user/{username}", status_code=200)
def get_user(username: str):
    """Endpoint to get a GitHub user's information."""
    user_info = github_client.get_user(username)
    return {"user_info": user_info}


@app.get("/org/{org_name}/repos", response_model=List[str])
def get_organization_repositories(org_name: str):
    """Endpoint to get a list of repositories for a given organization."""
    repos = github_client.list_organization_repositories(org_name)
    return repos
