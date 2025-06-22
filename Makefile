
SHELL := /bin/bash
# utils := @poetry run python -m scripts.utils
code := pyupdater *.py

format:  ## run autopep, ruff
	@uv run --frozen autopep8 --recursive --in-place $(code)
	# @uv run --frozen ruff check $(code) --select I001 --fix --quiet
	@uv run --frozen ruff check $(code) --quiet

.PHONY : lint
lint:  ## ruff linting
	@poetry run ruff check $(code)

clean:
	python dev/clean.py

deps:
	pip install -r requirements.txt --upgrade

deps-dev:
	pip install -r dev/requirements.txt --upgrade

api-md:
	python dev/api_docs.py

docs-deploy:
	mkdocs build --clean
	python dev/move.py

register:
	python setup.py register -r pypi

register-test:
	python setup.py register -r pypitest

test: clean
	tox
