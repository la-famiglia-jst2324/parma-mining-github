from fastapi import HTTPException
from github import Github, GithubException, Auth
from starlette import status

from parma_mining.github.model import OrganizationModel, RepositoryModel


class GitHubClient:
    def __init__(self, token: str):
        self.client = Github(auth=Auth.Token(token))

    # Retrieve organization details and statistics on all repositories of the organization
    def get_organization_details(self, org_name: str) -> OrganizationModel:
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
            )
