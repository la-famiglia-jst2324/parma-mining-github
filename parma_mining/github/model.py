"""Model for the GitHub data."""
import json
from datetime import datetime

from pydantic import BaseModel


class RepositoryModel(BaseModel):
    """Repository model for GitHub data."""

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
    watchers_count: int | None
    open_issues_count: int | None


class OrganizationModel(BaseModel):
    """Organization model for GitHub data."""

    name: str | None
    description: str | None
    url: str
    repos: list[RepositoryModel] | None
    aggregated_sum_size: int
    aggregated_sum_watchers_count: int
    aggregated_sum_open_issues_count: int
    aggregated_sum_stars: int
    aggregated_sum_forks: int

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
    """Discovery model for GitHub data."""

    name: str | None
    url: str | None


class CompaniesRequest(BaseModel):
    """Companies request model for GitHub data."""

    task_id: int
    companies: dict[str, dict[str, list[str]]]


class ResponseModel(BaseModel):
    """Response model for GitHub data."""

    source_name: str
    company_id: str
    raw_data: OrganizationModel


class ErrorInfoModel(BaseModel):
    """Error info for the crawling_finished endpoint."""

    error_type: str
    error_description: str


class CrawlingFinishedInputModel(BaseModel):
    """Internal base model for the crawling_finished endpoints."""

    task_id: int
    errors: dict[str, ErrorInfoModel] | None = None
