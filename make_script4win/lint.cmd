@echo off
echo Checking code quality...
uv run --directory backend ruff check app tests cli
uv run --directory backend ruff format app tests cli --check
uv run --directory backend mypy app