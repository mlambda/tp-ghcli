"""Command Line Interface (CLI) to interact with GitHub issues."""
import argparse

from .api import list_issues


def _create_parser() -> argparse.ArgumentParser:
    # Création du parseur d'arguments
    parser = argparse.ArgumentParser(
        description="GHCLI - CLI to list and create GitHub issues."
    )

    # Ajout de l'option owner avec une valeur par défaut qui pointe vers le dépôt git
    # du tp. L'autre option aurait été d'ajouter ici un argument (même syntaxe mais sans
    # les --). Il aurait alors été obligatoire de fournir une valeur pour appeler GHCLI
    parser.add_argument(
        "--owner", default="mlambda", help="Owner of the GitHub repository"
    )

    # Ajout de l'option repo avec une valeur par défaut qui pointe vers le dépôt git
    # du tp. L'autre option aurait été d'ajouter ici un argument (même syntaxe mais sans
    # les --). Il aurait alors été obligatoire de fournir une valeur pour appeler GHCLI
    parser.add_argument("--repo", default="tp-ghcli", help="GitHub repository")
    return parser


def main() -> None:
    """Parse CLI arguments and call the corresponding parts of GHCLI."""
    # Création du parseur d'arguments
    parser = _create_parser()

    # Récupération des arguments passés au programme
    args = parser.parse_args()

    # Utilisation de ces arguments
    list_issues(owner=args.owner, repo=args.repo)
