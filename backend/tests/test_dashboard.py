from unittest.mock import Mock


def create_user(client, email, password, role="viewer", token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return client.post(
        "/users/",
        json={"email": email, "password": password, "role": role},
        headers=headers,
    )

def login(client, email, password):
    return client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def seed_data(client):
    create_user(client, "admin@example.com", "Password123", "admin")
    admin_token = login(client, "admin@example.com",
                        "Password123").json()["access_token"]
    viewer = create_user(client, "viewer@example.com",
                         "Password123", "viewer", admin_token).json()
    analyst = create_user(client, "analyst@example.com",
                          "Password123", "analyst", admin_token).json()
    viewer_token = login(client, "viewer@example.com",
                         "Password123").json()["access_token"]
    analyst_token = login(client, "analyst@example.com",
                          "Password123").json()["access_token"]
    payloads = [
        {"amount": 3000, "type": "income",
            "category": "salary", "user_id": viewer["id"]},
        {"amount": 500, "type": "expense",
            "category": "rent", "user_id": viewer["id"]},
        {"amount": 200, "type": "expense",
            "category": "food", "user_id": viewer["id"]},
        {"amount": 1000, "type": "income",
            "category": "consulting", "user_id": analyst["id"]},
    ]
    for payload in payloads:
        response = client.post("/records/", json=payload,
                               headers=auth_headers(admin_token))
        assert response.status_code == 201
    return admin_token, analyst_token, viewer_token

def test_dashboard_role_scope_and_totals(client):
    admin_token, analyst_token, viewer_token = seed_data(client)
    viewer_dashboard = client.get(
        "/dashboard/", headers=auth_headers(viewer_token))
    assert viewer_dashboard.status_code == 403
    analyst_dashboard = client.get(
        "/dashboard/", headers=auth_headers(analyst_token))
    assert analyst_dashboard.status_code == 200
    analyst_data = analyst_dashboard.json()
    assert analyst_data["total_income"] == 4000
    assert analyst_data["total_expense"] == 700
    assert analyst_data["net_balance"] == 3300
    admin_dashboard = client.get(
        "/dashboard/", headers=auth_headers(admin_token))
    assert admin_dashboard.status_code == 200
    admin_data = admin_dashboard.json()
    assert admin_data["total_income"] == analyst_data["total_income"]
    assert admin_data["total_expense"] == analyst_data["total_expense"]

def test_dashboard_external_data_uses_mocked_http_call(client, monkeypatch):
    create_user(client, "admin@example.com", "Password123", "admin")
    token = login(client, "admin@example.com",
                  "Password123").json()["access_token"]
    mocked_response = Mock()
    mocked_response.raise_for_status.return_value = None
    mocked_response.json.return_value = {"base": "USD", "rates": {"EUR": 0.9}}
    monkeypatch.setattr("app.modules.dashboard.service.httpx.get",
                        lambda *args, **kwargs: mocked_response)
    response = client.get("/dashboard/external-data",
                          headers=auth_headers(token))
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["data"]["base"] == "USD"

def test_viewer_cannot_access_dashboard_external_data(client, monkeypatch):
    create_user(client, "admin@example.com", "Password123", "admin")
    admin_token = login(client, "admin@example.com",
                        "Password123").json()["access_token"]
    create_user(client, "viewer@example.com",
                "Password123", "viewer", admin_token)
    viewer_token = login(client, "viewer@example.com",
                         "Password123").json()["access_token"]
    mocked_response = Mock()
    mocked_response.raise_for_status.return_value = None
    mocked_response.json.return_value = {"base": "USD", "rates": {"EUR": 0.9}}
    monkeypatch.setattr("app.modules.dashboard.service.httpx.get",
                        lambda *args, **kwargs: mocked_response)
    response = client.get(
        "/dashboard/external-data", headers=auth_headers(viewer_token))
    assert response.status_code == 403
