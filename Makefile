PYTHON := python3
PIP := $(PYTHON) -m pip

setup:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: setup
	$(PYTHON) main.py
