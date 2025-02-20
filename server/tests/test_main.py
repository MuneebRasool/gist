"""
Tests for main application endpoints.
"""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """
    Test the root endpoint redirects to docs.
    """
    response = client.get("/")
    assert response.status_code == 200


def test_health_check(client: TestClient):
    """
    Test the health check endpoint returns correct response.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
