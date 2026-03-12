@echo off
echo Installing dependencies...
uv sync --directory backend --dev

echo.
echo one more dependency for win
uv pip install tzdata
echo ✅ Installation complete!
echo.
echo Next steps:
echo.  • make run              # Start development server
echo.
echo Note: backend/.env is pre-configured for development