"""GitHub client module."""
import logging

from fastapi import HTTPException, status
from github import Auth, Github, GithubException

from parma_mining.github.model import (
    DiscoveryResponse,
    OrganizationModel,
    RepositoryModel,
)
from parma_mining.mining_common.exceptions import CrawlingError

logger = logging.getLogger(__name__)


class GitHubClient:
    """GitHubClient class is used to fetch data from GitHub."""

    def __init__(self, token: str):
        """Initialize the GitHub client."""
        self.client = Github(auth=Auth.Token(token))

    def get_organization_details(self, org_name: str) -> OrganizationModel:
        """Get organization details and statistics.

        On all repositories of the organization.
        """
        try:
            organization = self.client.get_organization(org_name)
            org_info = {
                "name": organization.name,
                "description": organization.description,
                "url": organization.html_url,
                "repos": [],
                "aggregated_sum_size": 0,
                "aggregated_sum_watchers_count": 0,
                "aggregated_sum_open_issues_count": 0,
                "aggregated_sum_stars": 0,
                "aggregated_sum_forks": 0,
            }

            for repo in organization.get_repos():
                org_info["aggregated_sum_size"] += repo.size
                org_info["aggregated_sum_stars"] += repo.stargazers_count
                org_info["aggregated_sum_watchers_count"] += repo.watchers_count
                org_info["aggregated_sum_open_issues_count"] += repo.open_issues_count
                org_info["aggregated_sum_forks"] += repo.forks_count

                parsed_repo = RepositoryModel.model_validate(
                    {
                        "name": repo.name,
                        "description": repo.description or "",
                        "stars": repo.stargazers_count,
                        "forks": repo.forks_count,
                        "language": repo.language or "",
                        "created_at": repo.created_at.isoformat()
                        if repo.created_at
                        else None,
                        "updated_at": repo.updated_at.isoformat()
                        if repo.updated_at
                        else None,
                        "pushed_at": repo.pushed_at.isoformat()
                        if repo.pushed_at
                        else None,
                        "html_url": repo.html_url,
                        "clone_url": repo.clone_url,
                        "svn_url": repo.svn_url,
                        "homepage": repo.homepage or "",
                        "size": repo.size,
                        "watchers_count": repo.watchers_count,
                        "open_issues_count": repo.open_issues_count,
                    }
                )
                org_info["repos"].append(parsed_repo)

            return OrganizationModel.model_validate(org_info)
        except GithubException as e:
            msg = f"Error fetching organization details for {org_name}: {e}"
            logger.error(msg)
            raise CrawlingError(msg)

    def search_organizations(self, query: str) -> DiscoveryResponse:
        """Search organizations on GitHub."""
        try:
            organizations = self.client.search_users(query + " type:org")
            handles = []
            for org in organizations:
                handles.append(org.login)
            return DiscoveryResponse.model_validate({"handles": handles})

        except GithubException as e:
            logger.error(f"Error searching organizations for {query}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error searching organizations",
            )
