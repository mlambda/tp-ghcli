import typing

import pytest
import requests

from ghcli.api import create_issue, list_issues

TEST_OWNER = "mlambda"
GOOD_TEST_REPO = "tp-ghcli"
BAD_TEST_REPO = "i-do-not-exist"


@pytest.fixture
def bad_token(monkeypatch: typing.Any) -> None:
    monkeypatch.setenv("GHCLI_TOKEN", "bad_value")


@pytest.fixture
def mock_post(monkeypatch: typing.Any) -> None:
    class FakePost:
        def __init__(
            self,
            url: str,
            headers: typing.Dict[str, str],
            json: typing.Any,
            *args: typing.Any,
            **kwargs: typing.Any,
        ):
            if args:
                raise ValueError("Too many positional args")
            if kwargs:
                raise ValueError("Too many kw args")

        def raise_for_status(self) -> None:
            pass

        def json(self) -> typing.Dict[str, str]:
            return dict(
                title="Issue title",
                body="Issue body",
                html_url=f"https://github.com/{TEST_OWNER}/{GOOD_TEST_REPO}/issues/42",
            )

    monkeypatch.setattr(requests, "post", FakePost)


def test_list_issues_result_type() -> None:
    result = list_issues(TEST_OWNER, GOOD_TEST_REPO)
    assert isinstance(result, list)


def test_list_issues_html_url() -> None:
    issues = list_issues(TEST_OWNER, GOOD_TEST_REPO)
    assert all(GOOD_TEST_REPO in issue.url for issue in issues)


def test_list_issues_404() -> None:
    with pytest.raises(requests.HTTPError):
        list_issues(TEST_OWNER, BAD_TEST_REPO)


def test_create_issue(mock_post: typing.Any) -> None:
    issue = create_issue(TEST_OWNER, GOOD_TEST_REPO, "Issue title", "Issue body")
    assert issue.url == f"https://github.com/{TEST_OWNER}/{GOOD_TEST_REPO}/issues/42"


def test_create_issues_404() -> None:
    with pytest.raises(requests.HTTPError):
        create_issue(TEST_OWNER, BAD_TEST_REPO, "Issue title", "Issue body")


def test_create_issue_bad_token(bad_token: typing.Any) -> None:
    with pytest.raises(requests.HTTPError):
        create_issue(TEST_OWNER, GOOD_TEST_REPO, "Issue title", "Issue body")
