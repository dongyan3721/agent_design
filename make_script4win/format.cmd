@echo off
echo Formatting code...
uv run --directory backend ruff format app tests cli
uv run --directory backend ruff check app tests cli --fix