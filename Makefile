PYTHON := .venv/bin/python
VENV_DIR := .venv

.PHONY: agent_zero

agent_zero:
	@$(PYTHON) -m agent_zero.main