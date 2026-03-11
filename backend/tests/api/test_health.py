"""Health endpoint tests."""
from unittest.mock import AsyncMock
import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.anyio
async def test_health_check(client: AsyncClient):
    """Test liveness probe."""
    response = await client.get(f"{settings.API_V1_STR}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.anyio
async def test_readiness_check(client: AsyncClient):
    """Test readiness probe with mocked dependencies."""
    response = await client.get(f"{settings.API_V1_STR}/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["ready", "degraded"]
    assert "checks" in data

@pytest.mark.anyio
async def test_readiness_check_db_healthy(client: AsyncClient, mock_db_session):
    """Test readiness when MongoDB is healthy."""
    mock_db_session.command = AsyncMock(return_value={"ok": 1})

    response = await client.get(f"{settings.API_V1_STR}/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["checks"]["database"] is True


@pytest.mark.anyio
async def test_readiness_check_db_unhealthy(client: AsyncClient, mock_db_session):
    """Test readiness when MongoDB is unhealthy."""
    mock_db_session.command = AsyncMock(side_effect=Exception("MongoDB connection failed"))

    response = await client.get(f"{settings.API_V1_STR}/ready")
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert data["checks"]["database"] is False