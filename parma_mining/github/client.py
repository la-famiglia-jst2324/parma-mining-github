from github import Github, GithubException


class GitHubClient:
    def __init__(self, token):
        self.client = Github(token)

    def get_user(self, username=None):
        try:
            user = (
                self.client.get_user(username) if username else self.client.get_user()
            )
            return {
                "name": user.name,
                "email": user.email,
                "bio": user.bio,
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
            }
        except GithubException as e:
            # Handle exceptions from the GitHub API
            print(f"Error retrieving user: {e}")
            return None

    def list_repositories(self, username=None):
        try:
            user = self.get_user(username)
            return [repo.name for repo in user.get_repos()] if user else []
        except GithubException as e:
            # Handle exceptions from the GitHub API
            print(f"Error listing repositories: {e}")
            return []

    def list_organization_repositories(self, org_name):
        try:
            organization = self.client.get_organization(org_name)
            return [repo.name for repo in organization.get_repos()]
        except GithubException as e:
            # Handle exceptions or errors
            print(f"Error retrieving organization repositories: {e}")
            return []
