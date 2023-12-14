import json
from datetime import datetime

from pydantic import BaseModel


class RepositoryModel(BaseModel):
    """Model to structure the JSON Data."""

    name: str
    description: str | None
    stars: int | None
    forks: int | None
    language: str | None
    created_at: datetime | None
    updated_at: datetime | None
    pushed_at: datetime | None
    html_url: str | None
    clone_url: str | None
    svn_url: str | None
    homepage: str | None
    size: int | None
    stargazers_count: int | None
    watchers_count: int | None
    forks_count: int | None
    open_issues_count: int | None


class OrganizationModel(BaseModel):
    name: str | None
    description: str | None
    url: str
    repos: list[RepositoryModel] | None

    def updated_model_dump(self) -> str:
        """Dump the CompanyModel instance to a JSON string."""
        # Convert datetime objects to string representation
        json_serializable_dict = self.model_dump()
        repos = []
        if self.repos:
            for repo in self.repos:
                if repo:
                    repos.append(repo.model_dump())
        json_serializable_dict["repos"] = repos

        return json.dumps(json_serializable_dict, default=str)


class DiscoveryModel(BaseModel):
    name: str | None
    url: str | None


class CompaniesRequest(BaseModel):
    companies: dict[str, dict[str, list[str]]]


class ResponseModel(BaseModel):
    source_name: str
    company_id: str
    raw_data: OrganizationModel
