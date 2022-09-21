"""Interact with the GitHub API."""


def list_issues(owner: str, repo: str) -> None:
    """Retrieve issues of a GitHub repository."""
    print(f"Arguments récupérés par list_issues : owner={owner}, repo={repo}")
