
SHELL := /bin/bash
# utils := @poetry run python -m scripts.utils
code := pyupdater *.py

.PHONY : format
format:  ## autopep, isort, flake
	@poetry run autopep8 --recursive --in-place $(code)
	@poetry run isort $(code)
	@poetry run flake8 $(code)

.PHONY : flake
flake:  ## run flake with only selected dirs
	@poetry run flake8 $(code)

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
