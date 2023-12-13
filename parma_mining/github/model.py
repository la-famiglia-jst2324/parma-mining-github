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


class DiscoveryModel(BaseModel):
    name: str | None
    url: str | None


class CompaniesRequest(BaseModel):
    companies: dict[str, list[str]]
