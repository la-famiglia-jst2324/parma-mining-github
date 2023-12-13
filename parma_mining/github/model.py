import json
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
    name: Optional[str]
    url: Optional[str]


class CompaniesRequest(BaseModel):
    companies: dict[str, dict[str, list[str]]]


class ResponseModel(BaseModel):
    source_name: str
    company_id: str
    raw_data: OrganizationModel
