"""GitHub client module."""
import logging

from fastapi import HTTPException, status
from github import Auth, Github, GithubException

from parma_mining.github.model import DiscoveryModel, OrganizationModel, RepositoryModel

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
            }

            for repo in organization.get_repos():
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
                        "stargazers_count": repo.stargazers_count,
                        "watchers_count": repo.watchers_count,
                        "forks_count": repo.forks_count,
                        "open_issues_count": repo.open_issues_count,
                    }
                )
                org_info["repos"].append(parsed_repo)

            return OrganizationModel.model_validate(org_info)
        except GithubException as e:
            logger.error(f"Error fetching organization details for {org_name}: {e}")
            raise GithubException

    def search_organizations(self, query: str) -> list[DiscoveryModel]:
        """Search organizations on GitHub."""
        try:
            organizations = self.client.search_users(query + " type:org")
            return [
                DiscoveryModel.model_validate({"name": org.login, "url": org.html_url})
                for org in organizations
            ]
        except GithubException as e:
            logger.error(f"Error searching organizations for {query}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error searching organizations",
            )
