"""Interact with the GitHub API."""
import os
import sys


def _get_token() -> str:
    try:
        return os.environ["GHCLI_TOKEN"]
    except KeyError:
        print(
            "Impossible de récupérer le token GitHub dans la variable d'environnement "
            "GHCLI_TOKEN. Définissez cette variable et relancez le programme.",
            file=sys.stderr,
        )
        sys.exit(1)


def list_issues(owner: str, repo: str) -> None:
    """Retrieve issues of a GitHub repository."""
    print(f"Arguments récupérés par list_issues : owner={owner}, repo={repo}")
    token = _get_token()
    print(f"Token récupéré depuis _get_token : {token}")
