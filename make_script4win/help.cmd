@echo off
echo.
echo med_agent - Available Commands
echo ======================================
echo.
echo Setup:
echo.  make install       Install dependencies + pre-commit hooks
echo.
echo Development:
echo.  make run           Start dev server (with hot reload)
echo.  make test          Run tests
echo.  make lint          Check code quality
echo.  make format        Auto-format code
echo.
echo Users:
echo.  make create-admin  Create admin user (for SQLAdmin access)
echo.  make user-create   Create new user (interactive)
echo.  make user-list     List all users
echo.
echo Other:
echo.  make routes        Show all API routes
echo.  make clean         Clean cache files
echo.