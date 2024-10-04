"""Provide IO utilities."""

from collections.abc import Iterable
from json import dump
from pathlib import Path

from .model import Issue


def save_issues_to_file(issues: Iterable[Issue], file_path: Path) -> None:
    """
    Save issues to a file in JSON format.

    Args:
        issues: Iterable of issues to save.
        file_path: Path of the JSON output file.
    """
    data = [dict(title=issue.title, body=issue.body, url=issue.url) for issue in issues]
    with open(file_path, "w", encoding="utf8") as fh:
        dump(data, fh)
