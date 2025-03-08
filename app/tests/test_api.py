import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

@pytest.mark.parametrize("url, method", [
    ("/restaurants", "POST"),
    ("/restaurants/menus/", "POST"),
    ("/restaurants/menus/today/", "GET"),
    ("/votes", "POST"),
    ("/votes/today/", "GET"),
    ("/votes/results/today/", "GET"),
    ("/employees/1/", "GET"),
])
def test_endpoint_is_accessible(url, method):
    if method == "POST":
        response = client.post(url, json={})
    elif method == "GET":
        response = client.get(url)

    assert response.status_code != 404, f"Endpoint {url} not found"
    assert response.status_code == 401, f"Expected status 401, got {response.status_code} for endpoint {url}"


@pytest.mark.parametrize("url, method, data, expected_status", [
    ("/employees", "POST", {"username": "test",}, 422),
    ("/token", "POST", {"username": "test",}, 422),
])
def test_employee_user_endpoint_is_accessible(url, method, data, expected_status):
    if method == "POST":
        response = client.post(url, json=data)

    assert response.status_code != 404, f"Endpoint {url} not found"
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code} for endpoint {url}"


@pytest.mark.parametrize("url, method, data, expected_status", [
    ("/fake-endpoint", "GET", None, 404),
])
def test_fake_endpoint_is_not_accessible(url, method, data, expected_status):
    if method == "GET":
        response = client.get(url)

    assert response.status_code == 404, f"Expected status {expected_status}, got {response.status_code} for endpoint {url}"
