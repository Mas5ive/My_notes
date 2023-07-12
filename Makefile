install:
	poetry install

mynotes:
	poetry run mynotes


test:
	poetry run pytest


.PHONY: install test mynotes