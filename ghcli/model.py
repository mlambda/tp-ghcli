"""Model classes."""
import dataclasses
import typing


# Nous utilisons ici le module dataclasses de la bibliothèque standard qui permet de
# créer très vite de petites classes simples pour contenir des données de manière plus
# ordonnée qu'en utilisant des dictionnaires ou n-uplets
@dataclasses.dataclass
class Issue:
    """GitHub issue simple representation: only 3 attributes are kept."""

    title: str
    body: str
    url: str

    # L'ajout d'une méthode décorée par @classmethod permet de rendre cette méthode
    # appelable directement sur la classe :
    #     Issue.from_dict(...)
    # plutôt que :
    #     issue = Issue(...)
    #     issue.from_dict(...)
    # C'est très utile ici pour nous permettre de proposer un constructeur alternatif.
    # Le constructeur de base s'utilise de la manière suivante :
    #     Issue(title="Un titre", body="Un corps", url="https://une-url.com")
    # Alors que le constructeur que nous allons proposer ici pourra directement prendre
    # un dictionnaire tel que renvoyé par l'API GitHub et créer une issue à partir de
    # celui-ci.
    @classmethod
    def from_dict(cls, dct: typing.Dict[str, typing.Any]) -> "Issue":
        """Construct an issue from a dict such as one returned by GitHub API."""
        return Issue(title=dct["title"], body=dct["body"], url=dct["html_url"])
