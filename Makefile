SHELL := /bin/bash

CONDA_ENV != grep 'name:' environment.yml | sed 's/name://g' | sed -r 's/\s+//g'

# Solution based on https://blog.ianpreston.ca/conda/python/bash/2020/05/13/conda_envs.html
CONDA_ACTIVATE := source $$(conda info --base)/etc/profile.d/conda.sh; conda activate $(CONDA_ENV)

.PHONY: help
help:
	@echo "Commands:"
	@echo "conda-env    create development environment."
	@echo "pre-commit   install pre-commit hooks"
	@echo "style        run code style formatting."

.PHONY: conda-env
conda-env:
	conda env create && \
	conda env update -f environment-dev.yml

.PHONY: pre-commit
pre-commit:
	$(CONDA_ACTIVATE) && \
	pre-commit install && \
	pre-commit autoupdate

.PHONY: style
style:
	$(CONDA_ACTIVATE) && black .
	$(CONDA_ACTIVATE) && isort .
	$(CONDA_ACTIVATE) && flake8
