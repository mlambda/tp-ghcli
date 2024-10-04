"""Command Line Interface (CLI) to interact with GitHub issues."""

import argparse


def _add_repo_args(parser: argparse.ArgumentParser) -> None:
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


def _create_parser() -> argparse.ArgumentParser:
    # Création du parseur d'arguments
    parser = argparse.ArgumentParser(
        description="GHCLI - CLI to list and create GitHub issues."
    )

    # Création d'un objet subparsers. Celui-ci nous permettra de créer un parseur par
    # commande : un pour la commande list, un pour la commande create
    subparsers = parser.add_subparsers(help="Commands", dest="command")

    # Création du sous-parseur pour la commande list
    parser_list = subparsers.add_parser("list")
    # Ajout des arguments pour identifier le dépôt GitHub à cibler
    _add_repo_args(parser_list)

    # Création du sous-parseur pour la commande create
    parser_create = subparsers.add_parser("create")
    # Ajout des arguments pour identifier le dépôt GitHub à cibler
    _add_repo_args(parser_create)
    # Ajout des arguments qui permettent de spécifier le contenu de l'issue à créer
    parser_create.add_argument("title", help="Title of the GitHub issue")
    parser_create.add_argument("body", help="Body of the GitHub issue")

    return parser


def main() -> None:
    """Parse CLI arguments and call the corresponding parts of GHCLI."""
    # Création du parseur d'arguments
    parser = _create_parser()

    # Récupération des arguments passés au programme
    args = parser.parse_args()

    # Utilisation de ces arguments

    # D'abord, vérifions quelle commande a été appelée
    if args.command == "list":
        from .api import list_issues

        # Ensuite nous pouvons utiliser les arguments récupérer pour appeler la fonction
        # correspondante
        issues = list_issues(owner=args.owner, repo=args.repo)
        for issue in issues:
            print(f"{issue.url} - {issue.title} - {issue.body}")
    if args.command == "create":
        from .api import create_issue

        # Et de même pour la commande create
        issue = create_issue(
            owner=args.owner, repo=args.repo, title=args.title, body=args.body
        )
        print(f"{issue.url} - {issue.title} - {issue.body}")
    # Si aucune commande n'a été appelée, on lance l'IHM
    else:
        from .gui import create_gui

        create_gui()
