PYTHON_VERSION := python3.7
VIRTUALENV_DIR := venv



# Creating Virtual env
define create_venv
	if [[ -d "./${VIRTUALENV_DIR}" ]]; then \
		echo "Virtual env already exists"; \
	else \
		${PYTHON_VERSION} -m venv ${VIRTUALENV_DIR}; \
	fi
endef

# Activating Virtual env
define activate
	$(call create_venv) && source $(VIRTUALENV_DIR)/bin/activate
endef

# Installing Packages
define install_packages
	pip install -r requirements.frozen
endef

# Installing test Packages
define install_test_packages
	pip install -r requirements-test.txt
endef



.PHONY:clean build

clean::
	rm -rf $(VIRTUALENV_DIR) .cache .eggs .tmp *.egg-info ./*.egg-info
	find . -name ".DS_Store" -exec rm -rf {} \; || true
	find . -name "*.pyc" -exec rm -rf {} \; || true
	find . -name "__pycache__" -exec rm -rf {} \; || true
	find . -name "_cache" -exec rm -rf {} \; || true

build:	clean
	$(call create_venv) && \
	$(call activate) && \
	$(call install_packages)

test:
    python -m pytest tests
