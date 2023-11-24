from datetime import datetime
from pydantic import BaseModel
from typing import List


# Model to structure the JSON Data
class RepositoryModel(BaseModel):
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
