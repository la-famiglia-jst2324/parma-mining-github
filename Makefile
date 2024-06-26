.PHONY: prerequisites install dev test purge-db purge

# This Makefile should provide you with a simple way to get your dev
# environment up and running. It will install all the dependencies
# needed to run the project, and then run the project.

prerequisites:
	# Make sure to have micromamba installed - a fast conda/mamba implementation with very low overhead.
	# This will allow you to create a new environment with all the dependencies needed for this project.
	# Conda environments also contain dedicated python interpreters that won't mess up your local python installation."

install:
	pre-commit install
	micromamba create -f environment.yml  # Create a new environment
	# execute the following two steps manually
	# micromamba activate parma-mining-github  # Activate the new environment
	# pip install -e . # Install the project in editable mode

dev:
	uvicorn parma_mining.github.api:app --reload

test:
	pytest tests/

purge-db:
	# TODO

purge: purge-db
	rm -rf .mypy_cache .pytest_cache .coverage .eggs
