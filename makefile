# Makefile for running tests in a Django project

# Environment variables
PYTHON := python
MANAGE := $(PYTHON) manage.py
TESTS_DIR := tests

# Targets
.PHONY: test

test:
	$(MANAGE) test $(TESTS_DIR)
