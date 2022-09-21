check:
	black --check ghcli
	isort --check-only ghcli
	mypy ghcli
	flake8 --count
	pylint ghcli

.PHONY: check
