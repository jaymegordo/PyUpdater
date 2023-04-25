
SHELL := /bin/bash
# utils := @poetry run python -m scripts.utils
code := pyupdater *.py

.PHONY : format
format:  ## autopep, isort, ruff
	@poetry run autopep8 --recursive --in-place $(code)
	@poetry run isort $(code)
	@poetry run ruff check $(code)

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
