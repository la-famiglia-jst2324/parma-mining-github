from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class RepositoryModel(BaseModel):
    """Model to structure the JSON Data."""

    name: str
    description: Optional[str]
    stars: Optional[int]
    forks: Optional[int]
    language: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    pushed_at: Optional[datetime]
    html_url: Optional[str]
    clone_url: Optional[str]
    svn_url: Optional[str]
    homepage: Optional[str]
    size: Optional[int]
    stargazers_count: Optional[int]
    watchers_count: Optional[int]
    forks_count: Optional[int]
    open_issues_count: Optional[int]


class OrganizationModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    url: str
    repos: Optional[list[RepositoryModel]]


class DiscoveryModel(BaseModel):
    name: Optional[str]
    url: Optional[str]


class CompaniesRequest(BaseModel):
    companies: dict[str, dict[str, list[str]]]
