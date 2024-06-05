# Environment
ENV ?= dev

# GPU / CPU
PLATFORM ?= gpu

# IMAGE REPOSITORY
IMAGE_REPO ?= atomsci/atomsci-ampl

# Jupyter Port
JUPYTER_PORT ?= 8888

# Python Executable
PYTHON_BIN ?= $(shell which python)

# Virtual Environment
VENV ?= venv

# Work Directory
WORK_DIR ?= work

.PHONY: build-docker install install-system install-venv jupyter-notebook jupyter-lab pytest ruff ruff-fix setup uninstall uninstall-system uninstall-venv

# Pull Docker image
pull-docker:
	docker pull $(IMAGE_REPO):$(PLATFORM)-$(ENV)

# Push Docker image
push-docker:
	docker push $(IMAGE_REPO):$(PLATFORM)-$(ENV)

# Build Docker image
build-docker:
	@echo "Building Docker image for $(PLATFORM)"
	docker build -t $(IMAGE_REPO):$(PLATFORM)-$(ENV) --build-arg ENV=$(ENV) -f Dockerfile.$(PLATFORM) .

# Install atomsci-ampl system-wide
install: install-system

install-system:
	@echo "Installing atomsci-ampl into $(PYTHON_BIN)"
	$(PYTHON_BIN) -m pip install -e .

# Install atomsci-ampl in virtual environment
install-venv:
	@echo "Installing atomsci-ampl into $(VENV)/"
	$(VENV)/bin/python -m pip install -e .

# Run Jupyter Notebook
jupyter-notebook:
	@echo "Starting Jupyter Notebook"
	docker run -it -p $(JUPYTER_PORT):$(JUPYTER_PORT) \
		-v $(shell pwd)/$(WORK_DIR):/$(WORK_DIR) $(IMAGE_REPO):$(PLATFORM)-$(ENV) \
		/bin/bash -l -c "jupyter-notebook --ip=0.0.0.0 --allow-root --port=$(JUPYTER_PORT)"

# Run Jupyter Lab
jupyter-lab:
	@echo "Starting Jupyter Lab"
	docker run -it -p $(JUPYTER_PORT):$(JUPYTER_PORT) \
		-v $(shell pwd)/$(WORK_DIR):/$(WORK_DIR) $(IMAGE_REPO):$(PLATFORM)-$(ENV) \
		/bin/bash -l -c "jupyter-lab --ip=0.0.0.0 --allow-root --port=$(JUPYTER_PORT)"

# Run pytest
pytest:
	@echo "Running pytest"
	docker run -it -p $(JUPYTER_PORT):$(JUPYTER_PORT) \
		-v $(shell pwd)/$(WORK_DIR):/$(WORK_DIR) $(IMAGE_REPO):$(PLATFORM)-$(ENV) \
		/bin/bash -l -c "pytest"

# Run ruff linter
ruff:
	@echo "Running ruff"
	docker run -it $(IMAGE_REPO):$(PLATFORM)-$(ENV) /bin/bash -l -c "ruff check ."

# Run ruff linter with fix
ruff-fix:
	@echo "Running ruff with fix"
	docker run -it $(IMAGE_REPO):$(PLATFORM)-$(ENV) /bin/bash -l -c "ruff check . --fix"

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment with $(PLATFORM) dependencies"
	rm -rf $(VENV)/ || true
	python3.9 -m venv $(VENV)/
	$(VENV)/bin/pip install -U pip
	@echo "Installing dependencies"
	@if [ "$(PLATFORM)" = "gpu" ]; then \
		$(VENV)/bin/pip install -r pip/cuda_requirements.txt; \
	else \
		$(VENV)/bin/pip install -r pip/cpu_requirements.txt; \
	fi
	$(VENV)/bin/pip install -r pip/dev_requirements.txt
	$(MAKE) install

# Uninstall atomsci-ampl system-wide
uninstall: uninstall-system

uninstall-system:
	@echo "Uninstalling atomsci-ampl from $(PYTHON_BIN)"
	$(PYTHON_BIN) -m pip uninstall atomsci-ampl --yes

# Uninstall atomsci-ampl from virtual environment
uninstall-venv:
	@echo "Uninstalling atomsci-ampl from $(VENV)/"
	$(VENV)/bin/python -m pip uninstall atomsci-ampl --yes
