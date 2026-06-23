SHELL := /bin/bash

PYTHON ?= python3
SKILL_DIR ?= __SKILL_DIR__
CASE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPRO_CMD ?= true
TEST_CMD ?= $(REPRO_CMD)
RUN_ID ?= $(shell date +%Y%m%d-%H%M%S)
export TEST_CMD

.PHONY: help init build test env repro report bundle clean

help:
	@printf '%s\n' \
		'Compiler investigation case targets:' \
		'  make build                       Prepare case and capture compiler environment' \
		'  make test TEST_CMD="..."         Run and log a repro or validation command' \
		'  make report                      Render reports/report.md and report.html from captured evidence' \
		'  make bundle                      Create handoff tarball with checksums' \
		'  make clean                       Remove generated export bundles'

init:
	@mkdir -p problem tests/original tests/minimized tests/expected runs analysis reports export

build: init
	@$(PYTHON) "$(SKILL_DIR)/scripts/capture_env.py" --case-dir "$(CASE_DIR)"

test: init
	@$(PYTHON) "$(SKILL_DIR)/scripts/capture_run.py" --case-dir "$(CASE_DIR)" --run-id "$(RUN_ID)" --shell-env TEST_CMD

env: build

repro: test

report: init
	@$(PYTHON) "$(SKILL_DIR)/scripts/build_report.py" --case-dir "$(CASE_DIR)"

bundle: report
	@$(PYTHON) "$(SKILL_DIR)/scripts/export_bundle.py" --case-dir "$(CASE_DIR)"

clean:
	@rm -f export/*.tar.gz export/checksums.txt
