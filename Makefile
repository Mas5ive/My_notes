install:
# Check if Poetry is installed
ifeq (, $(shell which poetry))
	$(error "Poetry is not installed. Please install Poetry or use the install-pip command")
endif
	poetry install


install-pip:
	pip install -r requirements.txt


mynotes:
	poetry run mynotes


test:
	poetry run pytest


.PHONY: install install-pip test mynotes