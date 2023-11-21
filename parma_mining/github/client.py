from github import Github, GithubException


class GitHubClient:
    def __init__(self, token):
        self.client = Github(token)

    def get_user(self, username=None):
        try:
            # Use PyGithub to get the user
            return (
                self.client.get_user(username) if username else self.client.get_user()
            )
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
