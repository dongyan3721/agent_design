.PHONY: install format lint test run clean help db-init

# === Setup ===
install:
	uv sync --directory backend --dev
	@echo ""
	@echo "✅ Installation complete!"
	@echo ""
	@echo "Next steps:"	@echo "  • make run              # Start development server"	@echo ""
	@echo "Note: backend/.env is pre-configured for development"
# === Code Quality ===
format:
	uv run --directory backend ruff format app tests cli
	uv run --directory backend ruff check app tests cli --fix

lint:
	uv run --directory backend ruff check app tests cli
	uv run --directory backend ruff format app tests cli --check
	uv run --directory backend mypy app

# === Testing ===
test:
	uv run --directory backend pytest tests/ -v

test-cov:
	uv run --directory backend pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
# === Server ===
run:
	uv run --directory backend med_agent server run --reload

run-prod:
	uv run --directory backend med_agent server run --host 0.0.0.0 --port 8000

routes:
	uv run --directory backend med_agent server routes
# === Users ===
create-admin:
	@echo "Creating admin user..."
	uv run --directory backend med_agent user create-admin

user-create:
	uv run --directory backend med_agent user create

user-list:
	uv run --directory backend med_agent user list
# === Cleanup ===
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml

# === Help ===
help:
	@echo ""
	@echo "med_agent - Available Commands"
	@echo "======================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install dependencies + pre-commit hooks"
	@echo ""
	@echo "Development:"
	@echo "  make run           Start dev server (with hot reload)"
	@echo "  make test          Run tests"
	@echo "  make lint          Check code quality"
	@echo "  make format        Auto-format code"
	@echo ""	@echo "Users:"
	@echo "  make create-admin  Create admin user (for SQLAdmin access)"
	@echo "  make user-create   Create new user (interactive)"
	@echo "  make user-list     List all users"
	@echo ""	@echo "Other:"
	@echo "  make routes        Show all API routes"
	@echo "  make clean         Clean cache files"
	@echo ""
