.PHONY: validate validate-lite validate-max8000 test

PYTHON ?= python3

validate: validate-max8000 validate-lite

validate-max8000:
	PYTHONPATH=src $(PYTHON) -m libero_max validate-manifest benchmark/max8000/libero_max_8000.json

validate-lite:
	PYTHONPATH=src $(PYTHON) -m libero_max validate-manifest benchmark/lite/libero_max_lite.json

test:
	PYTHONPATH=src:. $(PYTHON) -m pytest -q
