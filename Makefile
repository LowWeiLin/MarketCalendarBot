.PHONY: install dev test run clean help

help:
	@echo "Market Calendar Bot - Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make dev       - Install with dev dependencies"
	@echo "  make test      - Run tests"
	@echo "  make run       - Run the bot"
	@echo "  make clean     - Clean cache files"
	@echo "  make lint      - Run linting checks"

install:
	uv sync --frozen

dev:
	uv sync

test:
	uv run pytest

run:
	uv run main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .uv_cache/

lint:
	uv run ruff check .
