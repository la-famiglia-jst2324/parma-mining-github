from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict


class RepositoryModel(BaseModel):
    """Model to structure the JSON Data."""

    name: str
    description: str
    stars: int
    forks: int
    language: str
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    html_url: str
    clone_url: str
    svn_url: str
    homepage: str
    size: int
    stargazers_count: int
    watchers_count: int
    forks_count: int
    open_issues_count: int


class OrganizationModel(BaseModel):
    name: str
    description: str
    url: str
    repos: List[RepositoryModel]


class DiscoveryModel(BaseModel):
    name: str
    url: str


class CompaniesRequest(BaseModel):
    companies: Dict[str, List[str]]


class OrganizationsResponse(BaseModel):
    organizations: List[OrganizationModel]
