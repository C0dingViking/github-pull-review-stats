PYTHON := python3
PIP := $(PYTHON) -m pip

.PHONY: run install

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) main.py
