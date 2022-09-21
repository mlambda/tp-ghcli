"""Interact with the GitHub API."""
import os
import sys
import typing

import deal
import requests

from .model import Issue


@deal.raises(SystemExit)
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


@deal.pre(lambda owner, repo: bool(owner) and bool(repo))
@deal.pre(lambda owner, repo: "/" not in owner)
@deal.pre(lambda owner, repo: "/" not in repo)
@deal.post(lambda issues: all(issue.url.startswith("http") for issue in issues))
@deal.raises(SystemExit, requests.HTTPError)
def list_issues(owner: str, repo: str) -> typing.List[Issue]:
    """Retrieve issues of a GitHub repository."""
    # Appel à l'API GitHub comme détaillé ici :
    # https://docs.github.com/en/rest/issues/issues#list-repository-issues
    # Cet appel permet d'obtenir un objet réponse de la bibliothèque requests :
    # https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/issues",
        headers=dict(
            Accept="application/vnd.github.v3+json",
            Authorization=f"token {_get_token()}",
        ),
    )

    # Vérifions d'abord qu'il n'y a pas eu de problème. Si la requête a renvoyé un code
    # d'erreur, une exception sera levée ici
    response.raise_for_status()

    # Nous pouvons maintenant récupérer le contenu de la réponse avec la méthode json.
    # Celle-ci va nous renvoyer une structure de données Python qui correspond au json
    # de la réponse. Ici, ce sera une liste de dictionnaires
    issues = response.json()

    # Nous créons enfin des objets Issue à l'aide de chaque dictionnaire
    return [Issue.from_dict(issue) for issue in issues]


@deal.pre(lambda owner, repo, title, body: bool(owner) and bool(repo))
@deal.pre(lambda owner, repo, title, body: "/" not in owner)
@deal.pre(lambda owner, repo, title, body: "/" not in repo)
@deal.post(lambda issue: issue.url.startswith("http"))
@deal.raises(requests.HTTPError, SystemExit)
def create_issue(owner: str, repo: str, title: str, body: str) -> Issue:
    """Retrieve issues of a GitHub repository."""
    # Appel à l'API GitHub comme détaillé ici :
    # https://docs.github.com/en/rest/issues/issues#create-an-issue
    # Cet appel permet d'obtenir un objet réponse de la bibliothèque requests :
    # https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
    response = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/issues",
        json=dict(title=title, body=body),
        headers=dict(
            Accept="application/vnd.github.v3+json",
            Authorization=f"token {_get_token()}",
        ),
    )

    # Vérifions d'abord qu'il n'y a pas eu de problème. Si la requête a renvoyé un code
    # d'erreur, une exception sera levée ici
    response.raise_for_status()

    # Nous pouvons maintenant récupérer le contenu de la réponse avec la méthode json.
    # Celle-ci va nous renvoyer une structure de données Python qui correspond au json
    # de la réponse. Ici, ce sera un dictionnaire
    issue = response.json()

    # Nous créons enfin un objet Issue à l'aide du dictionnaire
    return Issue.from_dict(issue)
