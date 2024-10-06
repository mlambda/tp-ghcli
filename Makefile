check:
	ruff check ghcli tests
	mypy ghcli tests

.PHONY: check
